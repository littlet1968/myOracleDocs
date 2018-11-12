#!/usr/bin/env python3
#
# from Tkinter import *
import requests
from bs4 import BeautifulSoup
import sys
import pdb
import json
import tkinter as tk
from time import sleep

progV = '0.0.1'
doc_url = 'https://oradocs-corp.documents.us2.oraclecloud.com/documents/'
login_base = 'https://login.oracle.com'
# login_url = 'https://login.oracle.com/oam/server/sso/auth_cred_submit'


class DocsDisplay(object):
    # display class for my littlet OraDocs program
    def __init__(self):
        self._setup_widgets()

    def _setup_widgets(self):
        # to top window
        self.top = tk.Tk()
        # and program description
        self.progl = tk.Label(self.top,
                              text="My little Oracle Documents V: %s" % progV)
        self.top.title("OraDocs")
        self.progl.pack()

        # the menu
        self.menu = tk.Menu(self.top)
        self.top.config(menu=self.menu)
        self.filemenu = tk.Menu(self.menu)
        self.menu.add_cascade(label='File', menu=self.filemenu)
        self.filemenu.add_command(label='Exit', command=self.top.quit)

        # the file list box
        self.filefm = tk.Frame(self.top)
        self.filesb = tk.Scrollbar(self.filefm)
        self.filesb.pack(side=tk.RIGHT, fill=tk.Y)
        self.filelb = tk.Listbox(self.filefm, height=15, width=50,
                                 yscrollcommand=self.filesb.set)
        self.filelb.bind('<Double-1>', self.selectEntry)
        self.filesb.config(command=self.filelb.yview)
        self.filelb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.filefm.pack(expand=True)

        self.messagefm = tk.Frame(self.top)
        self.messagesbV = tk.Scrollbar(self.messagefm)
        self.messagesbV.pack(side=tk.RIGHT, fill=tk.Y)
        self.messagesbH = tk.Scrollbar(self.messagefm, orient=tk.HORIZONTAL)
        self.messagesbH.pack(side=tk.BOTTOM, fill=tk.X)
        self.messagelb = tk.Listbox(self.messagefm, height=5, width=50,
                                    yscrollcommand=self.messagesbV.set,
                                    xscrollcommand=self.messagesbH.set)
        self.messagesbV.config(command=self.messagelb.yview)
        self.messagesbH.config(command=self.messagelb.xview)
        self.messagelb.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.messagefm.pack(expand=True)

        self.myJson = ""
        self.top.update()
        self.readConfig()

    def printMsg(self, message):
        self.messagelb.insert(tk.END, message)
        self.top.update()

    def readConfig(self, confFile=None):
            # read the configuration file for example username password
            # format =
            # { "ssousername": "oracle_user_name",
            #   "password": "oracle_SSO_password"}
            #
            # may other to come
            #
            if confFile is None:
                confFile = './config.json'
            with open(confFile) as json_file:
                json_data = json.load(json_file)
            try:
                self.login_data = {}
                self.login_data['ssousername'] = json_data['ssousername']
                self.login_data['password'] = json_data['password']
            except Exception as excp:
                print("Exception during configuration %s" % (excp))
                sys.exit
            # debug print(self.login_data)

    def openSession(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux i686) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/36.0.1985.125 Safari/537.36"}
        self.session = requests.Session()
        self.session.headers.update(self.header)
        self.session.max_redirects = 3

    def getAllInput(self, mySoup):
        # retrieve all imput vars from an soup object
        r_svars = {}
        # pdb.set_trace()
        for var in mySoup.findAll('input', type='hidden'):
            if var.has_attr('value'):
                r_svars[var['name']] = var['value']
        return r_svars

    def doSSO(self, page):
        # do the SSO login here since we might need some manual action
        self.printMsg('Doing SSO login')
        ssoURL = "https://login.oracle.com/mysso/signon.jsp"
        extURL = "https://login.oracle.com:443/oaam_server/oamLoginPage.jsp"

        try:
            # do we find the login some where int the URL
            # pdb.set_trace()
            while "login" in page.url:
                # pdb.set_trace()
                soup = BeautifulSoup(page.content, 'html.parser')
                allInput = {}
                allInput = self.getAllInput(soup)

                # first check if we have the the internal login page
                if soup.form.has_attr('action'):
                    if soup.form.attrs['action'] == ssoURL:
                        # looks like we are doing SSO from oracle network
                        # login via /oam/server/sso/auth_cred_submit
                        # so internal URL should be like that:
                        login_url = login_base + '/oam/server/sso/auth_cred_submit'
                        payload = {}
                        for key in allInput.keys():
                            payload[key] = allInput[key]
                            if key == "username":
                                payload[key] = self.login_data['ssousername']
                            if key == "password":
                                payload[key] = self.login_data['password']
                        # print(payload)
                        page = self.session.post(login_url, data=payload)
                    # are we coming from outside and need a redirect on login
                elif soup.form.attrs['action'] == extURL:
                        # looks like we are coming from outside
                        # the post url is like that
                        # /oam/server/sso/auth_cred_submit
                        # so internal URL should be like that:
                        login_url = soup.form.attrs['action']
                        payload = {}
                        payload = allInput
                        # print(payload)
                        page = self.session.post(login_url, data=payload)
                # second check if we have a "onload" in the body
                if soup.body.has_attr('onload'):
                    if soup.body['onload'] == "document.forms[0].submit();":
                        # if we have just a "press the submit button", doit
                        # and crate the payload to be posted
                        payload = {}
                        payload = allInput
                        # for key in allInput.keys():
                        #    payload[key] = allInput[key]
                        #    # the url that requested that
                        post_url = soup.form.attrs['action']
                        page = self.session.post(post_url, data=payload,
                                                 allow_redirects=True)
                if extURL in page.url:
                    myCookie = page.cookies['JSESSIONID']

            return page

        except Exception as excp:
            myMessage = 'Houston we have a problem ' + str(excp)
            self.printMsg(myMessage)

    def getToken(self):
        # try to get a token from the Oracle Docs server
        # returns true if successful
        #         SSO if login needed
        #         OAM if OAM logn needed (post SSO)
        docApi = '/web?IdcService=GET_OAUTH_TOKEN'
        token_url = doc_url + docApi

        # allInput = {}
        tok_page = self.session.get(token_url)
        # pdb.set_trace()
        if tok_page.status_code == requests.status_codes.codes.OK:
            # if we find login in the URL we most likely need to do a login
            if "login" in tok_page.url:
                print("going to SSO")
                tok_page = self.doSSO(tok_page)
                # if page.status_code != requests.status_codes.codes.OK:
                #    return "OUPS"
                print("return from SSO")
                print(type(tok_page))
            # workaround that the type returned is now after sso if not in
            # DEBUG
            if tok_page is None:
                tok_page = self.session.get(token_url)
            # print(type(tok_page))

            # either we reached here without need to login or we should be after
            if "IdcService" in tok_page.url:
                self.printMsg('Getting Oracle Docs Token')
                soup = BeautifulSoup(tok_page.content, 'html.parser')
                myJson = json.loads(str(soup))
                self.authToken = myJson['LocalData']['tokenValue']
                # update the header
                self.header["Authorization"] = "Bearer %s" %self.authToken
                self.session.headers.update(self.header)
                # pdb.set_trace()
                return self.authToken

    def docsInit(self):
        # gotSSO = False
        gotToken = False
        counterT = 0
        # open a new session
        self.openSession()
        # get a authentication token
        while True:
            counterT = counterT + 1
            if counterT > 4:
                self.printMsg('Failed to get Token')
                break
            # pdb.set_trace()
            gotToken = self.getToken()
            if gotToken:
                myMessage = 'Got Token' + str(gotToken)
                # self.printMsg(myMessage)
                break
        # get the root folder
        self.getFolder('/')

    def getFolder(self, folder):
        docApi = 'api/1.2/folders/'
        pdb.set_trace()

        if folder == '/':
            folder = 'items'
        else:
            newfolder = None
            for e in self.myJson["items"]:
                if e["name"] == folder:
                    newfolder = e["id"]
            if newfolder:
                folder = newfolder + "/items"
            else:
                folder = "items"

        urlApi = doc_url + docApi + folder
        page = self.session.get(urlApi)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.myJson = json.loads(str(soup))

        # delete all entries
        self.filelb.delete(0, tk.END)
        if folder != "items":
            self.filelb.insert(tk.END, '/..')
        for entry in self.myJson["items"]:
            if entry['type'] == 'folder':
                self.filelb.insert(tk.END, '/.' + entry['name'])
            else:
                self.filelb.insert(tk.END, '  ' + entry['name'])

        self.top.update()

    def getDocument(self):
        docApi = 'api/1.2/folders/'

    def selectEntry(self, ev=None):
        # docApi = 'api/1.2/folders/items'
        selEntry = self.filelb.get(self.filelb.curselection())
        pdb.set_trace()
        if selEntry[0:2] == '/.':
            self.printMsg(selEntry)
            # get the new folder entries
            self.getFolder(selEntry[2:])
        else:
            self.printMsg("Download")



def main():
    d = DocsDisplay()
    d.docsInit()
    # d.getDocument()
    tk.mainloop()


if __name__ == '__main__':
    main()

# session.close()
