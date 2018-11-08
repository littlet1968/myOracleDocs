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
# 'https://oradocs-corp.documents.us2.oraclecloud.com/documents
login_url = 'https://login.oracle.com/oam/server/sso/auth_cred_submit'
post_sso_url = 'https://login.us2.oraclecloud.com/oam/server/fed/sp/sso?tenant=corp'


class DocsDisplay(object):
    # display class for my littlet OraDocs program
    def __init__(self):
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
        # self.filelb.bind('<Double-1>', self.setDirAndGo)
        self.filesb.config(command=self.filelb.yview)
        self.filelb.pack(side=tk.LEFT, fill=tk.BOTH)
        self.filefm.pack()

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
        self.messagelb.pack(side=tk.LEFT, fill=tk.BOTH)
        self.messagefm.pack()

        self.myOraDocs = OraDocs()
        self.top.update()

    def doSSO(self):
        gotToken = False
        counterT = 0
        counterSSO = 0


    def docsInit(self):
        gotToken = False
        gotSSO = False
        counterT = 0
        while True:
            counterT = counterT + 1
            if counterT > 2:
                self.messagelb.insert(tk.END, 'Failed to get Token')
                self.top.update()
                break

            self.messagelb.insert(tk.END, 'Getting Oracle Docs Token')
            self.top.update()
            gotToken, page = self.myOraDocs.getToken()

            if gotToken == 'SSO':
                counterSSO = 0
                while True:
                    counterSSO = counterSSO + 1
                    if counterSSO > 2:
                        self.messagelb.insert(tk.END, 'SSO login failed')
                        self.top.update()
                        break

                    self.messagelb.insert(tk.END, 'Need SSO login')
                    self.top.update()
                    gotSSO, page = self.myOraDocs.checkSSOlogin(page)
                    if gotSSO == 'Done':
                        break
                    # sleep(10)

    def getDocument(self):
        docApi = 'api/1.2/folders/items'


class OraDocs(object):
    #
    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux i686) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/36.0.1985.125 Safari/537.36"}
        self.session = requests.Session()
        self.session.headers.update(self.header)
        self.res = False  # session results
        self.authToken = False  # our authentication token
        self.readConfig()

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

    def getAllInput(self, mySoup):
        # retrieve all imput vars from an soup object
        r_svars = {}
        for var in mySoup.findAll('input', type='hidden'):
            r_svars[var['name']] = var['value']
        return r_svars

    def checkSSOlogin(self, page):
        # check if the page is a SSO login page.
        login_success = False
        while login_success is False:
            soup = BeautifulSoup(page.content, 'html.parser')
            # do we find the login.oracle.com
            if "login.oracle.com" in soup.form.attrs['action']:
                # check if we are coming from outside
                if "oamLoginPage.jsp" in soup.form.attrs['action']:
                    # looks like we need to login to OAM first
                    print("OAM pre login_url")
                    login_url = soup.form.attrs['action']
                    payload = {}
                    allInput = {}
                    allInput = self.getAllInput(soup)
                    for key in allInput.keys():
                        payload[key] = allInput[key]
                    page = self.session.post(login_url, data=payload)

                # are we wait for SMS???
                # if
                # do the SSO login
                # login_url = soup.form.attrs['action']
                # allInput = {}
                # allInput = self.getAllInput(soup)
                #payload = {
                #    'OAM_REQ': allInput['OAM_REQ'],
                #    'locale': allInput['locale'],
                #    'request_id': allInput['request_id'],
                #    'contextType': allInput['contextType'],
                #    'resource_url': allInput['resource_url'],
                #}
                #payload = {}
                #for key in allInput.keys():
                #     payload[key] = allInput[key]
                ## print(payload)
                #payload['userid'] = self.login_data['ssousername']
                #payload['pass'] = self.login_data['password']
                #pdb.set_trace()
                #page = self.session.post(login_url, data=payload)
            #else:
                # looks like we don't have a login page
                #login_success = True
                #print("Login done or not needed")
                #return page  # as it is (now)

        return page  # return the new page

    def checkOAMlogin(self, page):
                # check if the page is a OAM login page.
                # first make it beautiful
                soup = BeautifulSoup(page.content, 'lxml')
                # do we find the login.oracle.com
                if "oraclecloud.com/oam/server" in soup.form.attrs['action']:
                    # do the SSO login
                    allInput = {}
                    allInput = self.getAllInput(soup)
                    payload = {}
                    for var in allInput.keys():
                        payload[var] = allInput[var]
                    # pdb.set_trace()
                    page = self.session.post(post_sso_url, data=payload)
                    return page  # return the new page
                else:
                    print("no login needed")
                    return page  # as it is

    def getToken(self):
        # try to get a token from the Oracle Docs server
        # returns true if successful
        #         SSO if login needed
        #         OAM if OAM logn needed (post SSO)
        docApi = '/web?IdcService=GET_OAUTH_TOKEN'
        token_url = doc_url + docApi

        allInput = {}
        page = self.session.get(token_url)
        pdb.set_trace()
        if page.status_code == requests.status_codes.codes.OK:
            soup = BeautifulSoup(page.content, 'html.parser')
            if 'login.oracle.com' in soup.form.attrs['action']:
                return 'SSO', page

            allInput = self.getAllInput(soup)
            pdb.set_trace()

        return 'OAM', page

    def getToken1(self):
        # try to get the token from the OraDocs
        # check if we have a token
        docApi = '/web?IdcService=GET_OAUTH_TOKEN'
        token_url = doc_url + docApi

        if not self.authToken:
            # try to open the web page
            try:
                # open the token page
                self.page = self.session.get(token_url)
                # check for problems
                self.page.raise_for_status()
                # if status is OK
                if self.page.status_code == requests.status_codes.codes.OK:
                    #pdb.set_trace()
                    # check if we need to do a SSO login
                    self.page = self.checkSSOlogin(self.page)
                    self.page.raise_for_status()
                    # just for the fun try it agin (debug)
                    # self.page = self.checkSSOlogin(self.page)

                    # check if we need to do a OAM login
                    self.page = self.checkOAMlogin(self.page)
                    self.page.raise_for_status()

                    # we should have now the token page now try to extract
                    soup = BeautifulSoup(self.page.content, 'html.parser')
                    try:
                        myJson = json.loads(str(soup))
                        self.authToken = myJson['LocalData']['tokenValue']
                        # update the header
                        self.header["Authorization"] = "Bearer %s" %self.authToken
                        self.session.headers.update(self.header)
                        # pdb.set_trace()
                        return self.authToken
                        # print(self.authToken)
                    except Exception as excp:
                        print("Exception trying to get token %s" % (excp))

                else:
                    raise Exception("Something got wrong getting token_url")

            except Exception as excp:
                print("The folowing problem occured: %s" % (excp))
        else:
            print("we got already a token %s" % (self.authToken))
            return self.authToken

    def getFiles(self):
        #doc_url = "https://oradocs-corp.documents.us2.oraclecloud.com/documents/api/1.2/folders/items"
        page = self.session.get(doc_url)
        print(page.content)

    def getHomeFolder(self):
        api = 'api/1.2/folders/items'
        self.page = self.session.get(doc_url + api)
        # pdb.set_trace()
        if self.page.status_code == requests.status_codes.codes.OK:
            soup = BeautifulSoup(self.page.content, 'html.parser')
            myJson = json.loads(str(soup))
            #pdb.set_trace()
            return myJson

    #def displayContent(self, myJson):
    #    # display the content


def main():
    # authToken = False
    d = DocsDisplay()
    d.docsInit()
    tk.mainloop()
    # myOraDocs = OraDocs()
    # myOraDocs.getToken()
    # myDocs = myOraDocs.getHomeFolder()
    # print(myDocs)
    # print(myOraDocs.res.content)
    # print(myOraDocs.page)
    # print(myOraDocs.page.content)


if __name__ == '__main__':
    main()

# session.close()
