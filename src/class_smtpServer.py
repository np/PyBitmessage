from pyelliptic.openssl import OpenSSL
import shared
import smtpd
import ssl
import time

from addresses import *
import helper_sent

class bitmessageSMTPServer(smtpd.SMTPServer):
    def __init__(self):
        # TODO - move to separate file/class
        smtpport = shared.config.getint('bitmessagesettings', 'smtpport')

        self.ssl = shared.config.getboolean('bitmessagesettings', 'smtpssl')
        if self.ssl:
            self.keyfile = shared.config.get('bitmessagesettings', 'keyfile')
            self.certfile = shared.config.get('bitmessagesettings', 'certfile')

        smtpd.SMTPServer.__init__(self, ('127.0.0.1', smtpport), None)
        shared.printLock.acquire()
        print "SMTP server started"
        shared.printLock.release()

    def handle_accept(self):
        # Override SMTPServer's handle_accept so that we can start an SSL connection.
        if not self.ssl:
            return smtpd.SMTPServer.handle_accept(self)

        sock, peer_address = self.accept()
        sock = ssl.wrap_socket(sock, server_side=True, certfile=self.certfile, keyfile=self.keyfile, ssl_version=ssl.PROTOCOL_SSLv23)
        channel = smtpd.SMTPChannel(self, sock, peer_address)

    def process_message(self, peer, mailfrom, rcpttos, data):
        #print("Peer", peer)
        #print("Mail From", mailfrom)
        #print("Rcpt To", rcpttos)
        #print("Data")
        #print(data)
        #print('--------')
        #print(type(mailfrom))

        message = data

        # Determine the fromAddress and make sure it's an owned identity
        # TODO - determine the address from a SMTP authorization.
        # TODO - use the mailfrom (a legitimate email address?) when delivering
        # real e-mail.
        _, fromAddress = mailfrom.split('@', 1)
        if not (fromAddress.startswith('BM-') and '.' not in fromAddress):
            raise Exception("From Address must be a Bitmessage address.")
        else:
            status, addressVersionNumber, streamNumber, fromRipe = decodeAddress(fromAddress)
            if status != 'success':
                shared.printLock.acquire()
                print 'Error: Could not decode address: ' + fromAddress + ' : ' + status
                if status == 'checksumfailed':
                    print 'Error: Checksum failed for address: ' + fromAddress
                if status == 'invalidcharacters':
                    print 'Error: Invalid characters in address: ' + fromAddress
                if status == 'versiontoohigh':
                    print 'Error: Address version number too high (or zero) in address: ' + fromAddress
                shared.printLock.release()
                raise Exception("Invalid Bitmessage address: {}".format(fromAddress))
            #fromAddress = addBMIfNotPresent(fromAddress) # I know there's a BM-, because it's required when using SMTP

            try:
                fromAddressEnabled = shared.config.getboolean(fromAddress, 'enabled')
            except:
                shared.printLock.acquire()
                print 'Error: Could not find your fromAddress in the keys.dat file.'
                shared.printLock.release()
                raise Exception("Could not find address in keys.dat: {}".format(fromAddress))
            if not fromAddressEnabled:
                shared.printLock.acquire()
                print 'Error: Your fromAddress is disabled. Cannot send.'
                shared.printLock.release()
                raise Exception("The fromAddress is disabled: {}".format(fromAddress))

        for recipient in rcpttos:
            _, toAddress = recipient.split('@', 1)
            if not (toAddress.startswith('BM-') and '.' not in toAddress):
                # TODO - deliver message to another SMTP server.. ?
                raise Exception("Cannot yet handle normal E-mail addresses.")
            else:
                # This is now the 3rd copy of this code. There's one in the API, there's another
                # copy in __init__ for the UI.  Yet another exists here.  It needs to be refactored
                # into a utility func!
                status, addressVersionNumber, streamNumber, toRipe = decodeAddress(toAddress)
                if status != 'success':
                    shared.printLock.acquire()
                    print 'Error: Could not decode address: ' + toAddress + ' : ' + status
                    if status == 'checksumfailed':
                        print 'Error: Checksum failed for address: ' + toAddress
                    if status == 'invalidcharacters':
                        print 'Error: Invalid characters in address: ' + toAddress
                    if status == 'versiontoohigh':
                        print 'Error: Address version number too high (or zero) in address: ' + toAddress
                    shared.printLock.release()
                    raise Exception("Invalid Bitmessage address: {}".format(toAddress))
                #toAddress = addBMIfNotPresent(toAddress) # I know there's a BM-, because it's required when using SMTP

                toAddressIsOK = False
                try:
                    shared.config.get(toAddress, 'enabled')
                    # The toAddress is one owned by me. We cannot send
                    # messages to ourselves without significant changes
                    # to the codebase.
                    shared.printLock.acquire()
                    print "Error: One of the addresses to which you are sending a message, {}, is yours. Unfortunately the Bitmessage client cannot process its own messages. Please try running a second client on a different computer or within a VM.".format(toAddress)
                    shared.printLock.release()
                except:
                    toAddressIsOK = True

                if not toAddressIsOK:
                    raise Exception("Cannot send message to {}".format(toAddress))

                # The subject is specially formatted to identify it from non-E-mail messages.
                subject = "<Bitmessage Mail: 00000000000000000000>" # Reserved, flags.

                ackdata = OpenSSL.rand(32)
                t = ('', toAddress, toRipe, fromAddress, subject, message, ackdata, int(time.time()), 'msgqueued', 1, 1, 'sent', 2)
                helper_sent.insert(t)

                toLabel = ''
                t = (toAddress,)
                shared.sqlLock.acquire()
                shared.sqlSubmitQueue.put('''select label from addressbook where address=?''')
                shared.sqlSubmitQueue.put(t)
                queryreturn = shared.sqlReturnQueue.get()
                shared.sqlLock.release()
                if queryreturn != []:
                    for row in queryreturn:
                        toLabel, = row
                shared.UISignalQueue.put(('displayNewSentMessage', (toAddress, toLabel, fromAddress, subject, message, ackdata)))
                shared.workerQueue.put(('sendmessage', toAddress))

                # TODO - what should we do with ackdata.encode('hex') ?


