# TODO
# what's up with paperclip? how to copy
# select instead of copy?
# pos data code
# tlv parsing with lambda
# 

import sublime
import os, re
import sys
# Zemlyanoi-PC
# sys.path.insert(0, 'D:\\Users\\nikolaev_v\\AppData\\Local\\Programs\\Python\\Python36-32\\Lib\\site-packages')
# import pyperclip
import sublime_plugin
from collections import namedtuple

# DEBUG = 1
DEBUG = 0

TVR_LEN = 10
CVR_MC_LEN = 12
TSI_LEN =  4
D5_LEN = 5
BICISO_FLAGS_LEN = 31
NEW_LINE = '\n'

# html tags
TAG_BR   = '<br>'
TAG_I_A  = '<i>'
TAG_I_Z  = '</i>'
TAG_LI_A = '<li>'
TAG_LI_Z = '</li>'
TAG_U_A  = '<u>'
TAG_U_Z  = '</u>'
TAG_UL_A = '<ul>'
TAG_UL_Z = '</ul>'

# EMV tags definition files 
FILES_RELATIVE_PATH = "Packages/User/EMV_TAGS/"
FILE_TVR          = FILES_RELATIVE_PATH + "TVR.txt"
FILE_TSI          = FILES_RELATIVE_PATH + "TSI.txt"
FILE_TSI          = FILES_RELATIVE_PATH + "TSI.txt"
FILE_DISAB        = FILES_RELATIVE_PATH + "disab_stat.txt"
FILE_WARN         = FILES_RELATIVE_PATH + "warn_stat.txt"
FILE_CONFIG       = FILES_RELATIVE_PATH + "hw_config.txt"
FILE_CVR_MC       = FILES_RELATIVE_PATH + "CVR_MC.txt"
FILE_CVR_VI_VIS   = FILES_RELATIVE_PATH + "CVR_VI_VIS.txt"
FILE_CVR_VI_CCD   = FILES_RELATIVE_PATH + "CVR_VI_CCD.txt"
FILE_HEADER       = FILES_RELATIVE_PATH + "curr_transHeaderFlags.txt"
FILE_D5           = FILES_RELATIVE_PATH + "D5.txt"
FILE_BICISO_FLAGS = FILES_RELATIVE_PATH + "biciso_flags.txt"

# pos data code definition

definition = namedtuple("definition", ["value", "key", "description", "description2"])
# /* Defines for card data input capability (position 1) */
cardDataInputCapability = [
  definition("TICI_UNKNOWN"                         , "0",  "Неизвестно", "unknown"),
  definition("TICI_NO_TERMINAL"                     , "1",  "Ручной ввод, терминал отсутствует", "manual, no terminal"),
  definition("TICI_MAG_STRIPE_READER"               , "2",  "Чтение магнитной полосы", "magnetic stripe read"),
  definition("TICI_BAR_CODE_READER"                 , "3",  "Чтение штрихкода", "bar code read"),
  definition("TICI_OCR_READER"                      , "4",  "OCR (оптическое распознавание образов)", "OCR read"),
  definition("TICI_MAG_AND_ICC"                     , "5",  "Чтение чипа, магнитной полосы", "magnetic stripe read and EMV-compatible ICC reader"),
  definition("TICI_KEYENTRY"                        , "6",  "Ручной ввод с использованием терминала", "key entered"),
  definition("TICI_MAG_AND_KEYENTRY"                , "7",  "Чтение магнитной полосы и ручной ввод с использованием терминала", "key entered and magnetic stripe read"),
  definition("TICI_MAG_KEYENTRY_AND_ICC"            , "8",  "Чтение магнитной полосы, чипа и ручной ввод с использованием терминала", "magnetic stripe reader, key entry and EMV compatible ICC reader"),
  definition("TICI_ONLY_CONTACTLESS_ALL"            , "9",  "Чтение только бесконтактных карт. По образу чипа и по образу магнитной полосы", "Only Contactless: ICC & magstripe"),
  definition("TICI_CONTACT_AND_CONTACTLESS_STRIPE"  , "A",  "Чтение контактного чипа и чтение бесконтактных карт по образу магнитной полосы", "Contact: ICC; Contactless: magstripe"),
  definition("TICI_ONLY_CONTACTLESS_STRIPE"         , "B",  "Чтение только бесконтактных карт по образу магнитной полосы", "Only Contactless: magstripe"),
  definition("TICI_CONTACT_AND_CONTACTLESS_ALL"     , "M",  "Чтение контактного чипа и бесконтактных карт по образу сипа и магнитной полосы", "Contact: ICC; Contactless: ICC & magstripe"),
]


# /* Defines for cardholder authentication capability (position 2) */
cardholderAuthenticationCapability = [
  definition("NO_ELECTRONIC_AUTHENTICATION" , "0", "Возможность электронной аутентификации отсутствует", "No electronic authentication"),
  definition("PIN"                          , "1", "Присутствует возможность аутентификации с использованием PIN", "Pin"),
  definition("ELECTRONIC_SIGN_ANALYSIS"     , "2", "Возможность аутентификации с помощью анализа электронной подписи", "Electronic signature analysis"),
  definition("BIOMETRICS"                   , "3", "Возможность аутентификации с помощью биометрических данных", "Biometrics"),
  definition("BIOGRAPHICS"                  , "4", "Возможность аутентификации с помощью биографических данных", "Biographics"),
  definition("ELECTRONIC_AUTH_INOPER"       , "5", "Электронная аутентификация", "Electronic authentication inoperative"),
  definition("OTHER"                        , "6", "Другое", "Other"),
  definition("RESERVED_1"                   , "7", "--", "Reserved for future use"),
  definition("RESERVED_2"                   , "8", "--", "Reserved for future use"),
  definition("AUTH_VALUE"                   , "9", "Возможность аутентификации с помощью authentication value", "Authentication value"),
]

# /* Defines for card capture capability (position 3) */
cardCaptureCapability = [
  definition("CCC_NONE"               , "0", "Отсутствует возможность захвата карты", "None"),
  definition("CCC_CAPTURE"            , "1", "Присутствует возможность захвата карты", "Capture"),
]

# /* Defines for operating environment (position 4) */
operatingEnvironment = [
  definition("OE_NO_TERM"                                  , "0", "Терминал отсутствует", "No terminal used"),
  definition("OE_ON_PREMISES_OF_CARD_ACCEPTOR_ATTENDED"    , "1", "Терминал находится на территории торговой организации, задействован обслуживающий персонал", "On premises of card acceptor, attended"),
  definition("OE_ON_PREMISES_OF_CARD_ACCEPTOR_UNATTENDED"  , "2", "Терминал самообслуживания находится на территории торговой организации", "On premises of card acceptor, untended"),
  definition("OE_OFF_PREMISES_OF_CARD_ACCEPTOR_ATTENDED"   , "3", "Терминал находится вне территории торговой организации, задействован обслуживающий персонал", "Off premises of card acceptor, attended"),
  definition("OE_OFF_PREMISES_OF_CARD_ACCEPTOR_UNATTENDED" , "4", "Терминал самообслуживания находится вне территории торговой организации", "Off premises of card acceptor, unattended"),
  definition("OE_ON_PREMISES_OF_CARDHOLDER_UNATTENDED"     , "5", "Терминал самообслуживания находится на территории держателя карты", "On premises of card cardholder, unattended"),
  definition("OE_CAT_LEVEL_0_UNATTENDED"                   , "R", "", "CAT level 0, unattended"),
  definition("OE_CAT_LEVEL_1_UNATTENDED"                   , "S", "", "CAT level 1, unattended"),
  definition("OE_CAT_LEVEL_2_UNATTENDED"                   , "T", "", "CAT level 2, unattended"),
  definition("OE_CAT_LEVEL_3_UNATTENDED"                   , "U", "", "CAT level 3, unattended"),
  definition("OE_CAT_LEVEL_4_UNATTENDED"                   , "V", "", "CAT level 4, unattended"),
  definition("OE_CAT_LEVEL_5_UNATTENDED"                   , "W", "", "CAT level 5, unattended"),
  definition("OE_CAT_LEVEL_6_UNATTENDED"                   , "X", "", "CAT level 6, unattended"),
  definition("OE_CAT_LEVEL_7_UNATTENDED"                   , "Y", "", "CAT level 7, unattended"),
  definition("OE_CAT_LEVEL_9_UNATTENDED"                   , "9", "CAT level 9, Mobile POS", "CAT level 9, Mobile POS"),
]

# /* Defines for POS cardholder presence indicator (position 5) */
POSCardholderPresenseIndicator = [
  definition("PCPI_PRESENT"           , "0", "Держатель карты присутствует", ""),
  definition("PCPI_UNCPECIFIED"       , "1", "Держатель карты отсутствует, причины не уточняются", ""),
  definition("PCPI_MAIL_ORDER"        , "2", "Держатель карты отсутствует, заказ по почте", ""),
  definition("PCPI_TELEPHONE_ORDER"   , "3", "Держатель карты отсутствует, заказ по телефону", ""),
  definition("PCPI_STANDING_ORDER"    , "4", "Держатель карты отсутствует, регулярный платёж", ""),
  definition("PCPI_ELECTRONIC_ORDER"  , "5", "Держатель карты отсутствует, электронная коммерция", ""),
]

# /* Defines for card presence (position 6) */
cardPresense = [
  definition("CPI_NOT_PRESENT"               , "0", "Карта отсутствует", ""),
  definition("CPI_PRESENT"                   , "1", "Карта присутствует", ""),
  definition("CPI_NOT_PRESENT_TOKEN_PRESENT" , "2", "Присутствует токенизированный номер карты", ""),
]

# /* Defines for card data input mode (position 7) */
cardDataIpputMode = [
  definition("UNSPECIFIED"                 , "0", "Не уточняется", ""),
  definition("MANUAL"                      , "1", "Ручной ввод без терминала", ""),
  definition("MAGNETIC_STRIPE_READ"        , "2", "Считывание магнитной полосы", ""),
  definition("BAR"                         , "3", "Считывание штрих кода", ""),
  definition("OCR"                         , "4", "Считывание посредством OCR (оптическое распознавание образов)", ""),
  definition("ICC"                         , "5", "Считывание чипа", ""),
  definition("KEY_ENTERED"                 , "6", "Ручной ввод на терминале", ""),
  definition("CONTACTLESS_ICC"             , "7", "Бесконтактное считывание чипа с использованием чиповых данных", ""),
  definition("CONTACTLESS_MAGNETIC_STRIPE" , "8", "Бесконтактное считывание чипа с использованием данных магнитной полосы", ""),
  definition("CONTACTLESS_READ"            , "9", "Бесконтактное считывание", ""),
  definition("EC_CHANNEL_DSRP"             , "D", "Транзакции с использованием технологии Digital Secure Remote Payment", ""),
  definition("CREDENTIAL_ON_FILE"          , "F", "Транзакции с использованием ранее сохранённых мерчантом данных карты", ""),
  definition("CARDLESS_GIRO"               , "G", "Данные карты получены с помощью сервиса GIRO", ""),
  definition("MP_CHANNEL_ENC"              , "M", "Транзакции MasterPass", ""),
  definition("EC_NO_SECURITY"              , "U", "", ""),
  definition("EC_CHANNEL_ENC"              , "V", "", ""),
  definition("EC_INCL_REMOTE_CHIP"         , "R", "Транзакции электронной коммерции, включая remote chip", "E-commerce, including remote chip"),
  definition("EC_SET_MERCH_CERT"           , "S", "Транзакции электронной коммерции в точке, поддерживающей 3-D Secure, но без его использования", ""),
  definition("EC_SET_MERCH_CRDH_CERT"      , "T", "Транзакции электронной коммерции в точке, поддерживающей 3-D Secure с его использованием", ""),
  definition("AUTOMATIC"                   , "W", "Автоматический ввод данных, сохранённых ранеев сторонней системе", ""),
  definition("EC_MERCH_TRUST"              , "X", "Транзакция электронной коммерции, проводимая с доверенного мерчанта", ""),
]

# /* Defines for cardholder authentification method (position 8) */
cardholderAuthentificationMethod = [
  definition("CAM_NOT_AUTH"              , "0", "Аутентификация не проводилась", "Not authenticated"),
  definition("CAM_PIN"                   , "1", "Аутентификация с использованием PIN", "PIN"),
  definition("CAM_OFFLINE_PIN"           , "3", "Аутентификация с использованием оффлайн PIN", "offline PIN authentication"),
  definition("CAM_MANUAL_SIGNATURE"      , "5", "Аутентификация с использованием рукописной подписи", "Manual signature verification"),
  definition("CAM_OTHER_MANUAL"          , "6", "Другой способ аутентификации", "Other manual verification"),
  definition("CAM_PASSCODE"              , "A", "Аутентификация с использованием passcode на устройстве", ""),
  definition("CAM_BIOMETRIC"             , "B", "Аутентификация с использованием биометрических данных", ""),
  definition("CAM_DEVICE_CODE"           , "C", "Аутентификация с помощью кода, вводимого на устройстве", ""),
  definition("CAM_DEVICE_PATTERN"        , "D", "Аутентификация с помощью графического ключа, вводимого на устройстве", ""),
  definition("CAM_EC_PARTIAL"            , "P", "Partial shipment or recurring payment", ""),
  definition("CAM_ISSUER_RBD"            , "Q", "Issuer risk based decisioning", "Issuer risk based decisioning"),
  definition("CAM_MERCH_RBD"             , "R", "Merchant risk based decisioning", "Merchant risk based decisioning"),
  definition("UCAF_3DS_STATIC_AAV"       , "S", "Аутентификация с использованием Static AVV", "Static AAV"),
  definition("UCAF_3DS_MERCH_NOT_SUP"    , "T", "Электронная коммерция, электронная аутентификация по протоколу безопасности не поддерживается", "UCAF not supported by merchant"),
  definition("UCAF_3DS_ISS_NOT_SUP"      , "U", "Электронная коммерция, 3D Secure аутентификация поддерживается точкой, но не поддерживается эмитентом", "UCAF supported by merchant but not provided by issuer"),
  definition("UCAF_3DS_AUTH"             , "V", "Электронная коммерция, успешная аутентификация по 3DS", "UCAF is present"),
  definition("CAM_EC_3DS_ATTEMPT"        , "W", "Электронная коммерция, попытка аутентификации по 3DS", "3Ds authentication attempted"),
  definition("CAM_EC_MERCH_AUTH"         , "X", "Электронная коммерция, аутентификация средствами мерчанта", "EC authentication by merchant"),
]

# /* Defines for cardholder authentication entity (position 9) */
cardholderAuthenticationEntry = [
  definition("CAE_NOT_AUTH"              , "0", "Без аутентификации", "Not authenticated"),
  definition("CAE_ICC"                   , "1", "Аутентификация с использованием чипа - оффлайн PIN", "ICC"),
  definition("CAE_AUTH_AGENT"            , "3", "Аутентификация у эмитента (система авторизации) - online PIN", "Authorizing agent"),
  definition("CAE_BY_MERCHANT"           , "4", "Аутентификация у эквайера - рукописная подпись", "By merchant"),
  definition("CAE_OTHER"                 , "5", "Другая аутентификация", "Other"),
  definition("CAE_DEVICE"                , "D", "Аутентификация на устройстве", "Device auth"),
  definition("CAE_MERCH_SUSP"            , "S", "Подозрение со стороны мерчанта", "Merchant suspicious"),
]

# /* Defines for card data output capability (position 10) */
cardDataOutputCapability = [
  definition("COC_UNKNOWN"               , "0", "Неизвестен", "Unknown"),
  definition("COC_NONE"                  , "1", "Отсутствует", "None"),
  definition("COC_ICC"                   , "3", "Вывод на чип", "ICC"),
]

# /* Defines for terminal output capability (position 11) */
terminalOutputCapability = [
  definition("TOC_UNKNOWN"               , "0", "Информация о способах вывода отсутствует", "Unknown"),
  definition("TOC_NONE"                  , "1", "Возможность вывода на терминале отсутствует", "None"),
  definition("TOC_PRINT"                 , "2", "Возможен вывод на печатающее устройство", "Printing"),
  definition("TOC_DISPLAY"               , "3", "Возможен вывод на дисплей", "Display"),
  definition("TOC_PRINT_AND_DISPLAY"     , "4", "Возможен вывод на печатающее устройство или на дисплей", "Printing and display"),
  definition("TOC_NO_CASHBACK"           , "5", "Терминал не поддерживает cashback", "Terminal do not support cashback"),
]

# /* Defines for PIN capture capability (position 12)*/
PINCaptureCapability = [
  definition("PINCC_NO"                  ,  "0", "PIN не обрабатывается", "No PIN capture capability"),
  definition("PINCC_UNKNOWN"             ,  "1", "Неизвестно", "Unknown"),
  definition("PINCC_4"                   ,  "4", "обрабатывается PIN до 4 цифр", "Four characters"),
  definition("PINCC_6"                   ,  "6", "обрабатывается PIN до 6 цифр", "Six characters"),
  definition("PINCC_12"                  , "12", "обрабатывается PIN до 12 цифр", "Six characters"),
]

pos_data_code = [
  cardDataInputCapability,
  cardholderAuthenticationCapability,
  cardCaptureCapability,
  operatingEnvironment,
  POSCardholderPresenseIndicator,
  cardPresense,
  cardDataIpputMode,
  cardholderAuthentificationMethod,
  cardholderAuthenticationEntry,
  cardDataOutputCapability,
  terminalOutputCapability,
  PINCaptureCapability,
]

def dprint(log):
  if DEBUG:
    print(log)
  # if

class ParseBinaryCommand(sublime_plugin.TextCommand):
    def done(self):
      dprint("done")
      return

    def check_hex(self):
      dprint("check_hex")
      word=self.word
      v=self.view
      if re.search("[^0-9A-F]",word):
        content = 'only 0123456789ABCDEF accepted'
        v.show_popup(content)
        return 0
      # if
      return 1

    def parseDef(self):
      odd = 1
      content = ''
      dprint("parseDef: 1")
      for letter in self.word :
        content = content + (str(odd/2+.5)[:1] if odd % 2 else '')
        content = content + ' ' + bin(int(letter, 16))[2:].zfill(4) 
        odd += 1
        content += TAG_BR if odd % 2 else ''
        if odd > 20:
          content += TAG_BR + 'too much symbols'
          break
      # for

      link = '<a href="' + re.sub(TAG_BR,NEW_LINE,content) + '">copy me</a>'
      content += link
      self.view.show_popup(content, on_navigate=self.navigate)
      pass

##########
# not needed, just for future testing purposes
    def parseTVR(self):
      dprint("parseTVR")
      if self.check_hex() != 1:
        return
      # if

      bits = ''
      counter = 0
      word = self.word 
      for letter in word:
        bits += bin(int(letter, 16))[2:].zfill(4) 
      # for

      # content = sublime.load_resource("Packages/User/TVR.html")
      # m = re.findall(r"((?<=<li>).*(?=</li>))+?", content)

      m = re.split(NEW_LINE, sublime.load_resource("Packages/User/EMV_TAGS/TVR.txt"))
      if len(m) <= 0:
        self.view.show_popup('file not found or empty?', on_navigate=self.navigate)
        return
      # if

      content = ''

      for bit in bits:
        # doesn't work, don't know why
        if counter > len(m) - 1:
          # if counter % 8 != 0:
          #   content += TAG_UL_Z + NEW_LINE
          break
        # if

        if counter % 8 == 0:
          content += TAG_UL_A + NEW_LINE
        # if

        if bit == '1':
          content += TAG_LI_A + TAG_U_A + TAG_I_A + '1 ' + m[counter] + TAG_I_Z + TAG_U_Z + TAG_LI_Z + NEW_LINE
        elif bit == '0':
          content += TAG_LI_A + '0 ' + m[counter] + TAG_LI_Z + NEW_LINE
        else:
          self.view.show_popup("We must not be here.")
          return
        # if

        counter += 1
        if counter % 8 == 0:
          content += TAG_UL_Z + NEW_LINE
        # if
      # for 

      dprint(content)

      self.view.show_popup(content, max_width=1000, max_height=1000)
      return
# not needed, just for future testing purposes
##########



    def parseTag(self, filename, min_length, max_length):
      dprint("parseTag")
      if self.check_hex() != 1:
        return
      # if
      dprint("0")

      bits = ''
      counter = 0
      word = self.word 
      for letter in word:
        bits += bin(int(letter, 16))[2:].zfill(4) 
      # for

      # content = sublime.load_resource("Packages/User/TVR.html")
      # m = re.findall(r"((?<=<li>).*(?=</li>))+?", content)

      m = re.split(NEW_LINE, sublime.load_resource(filename))
      dprint(len(m))
      
      if len(m) <= 0:
        self.view.show_popup('file not found', on_navigate=self.navigate)
        return
      # if

      content = ''

      for bit in bits:
        if counter > len(m) - 1:
          break
        # if

        if counter % 8 == 0:
          content += TAG_UL_A + NEW_LINE
        # if

        if bit == '1':
          content += TAG_LI_A + TAG_U_A + TAG_I_A + '1 ' + m[counter] + TAG_I_Z + TAG_U_Z + TAG_LI_Z + NEW_LINE
        elif bit == '0':
          content += TAG_LI_A + '0 ' + m[counter] + TAG_LI_Z + NEW_LINE
        else:
          self.view.show_popup("We must not be here.")
          return
        # if

        counter += 1
        if counter % 8 == 0:
          content += TAG_UL_Z + NEW_LINE
        # if
      # for 

      dprint(content)

      self.view.show_popup(content, max_width=1000, max_height=1000)
      return

    def parseCVRVisa(self):
      dprint("parseCVRVisa")
      if self.check_hex() != 1:
        return
      # if
      return

    def parseCVRMaster(self):
      dprint("parseCVRMaster")
      if self.check_hex() != 1:
        return
      # if
      return

    def parseTLV(self):
      dprint("parseTLV: 1")
      if self.check_hex() != 1:
        return
      # if

      content = ''
      word = self.word
      length = len(word)
      pointer = 0
      dprint(length)
      if length %2 == 1:
        print("odd senses!")
        return
      # if
      while pointer != length:
        tag_id = word[length - (length - pointer):length - (length - pointer) + 2]
        pointer += 2
        if ( (int(tag_id,16) & 0x1f) == 0x1f ):
          dprint("double tag")
          tag_id += word[length - (length - pointer):length - (length - pointer) + 2]
          pointer += 2
        # if
        content += tag_id.ljust(5)

        tag_len = int(word[length - (length - pointer):length - (length - pointer) + 2], 16) * 2
        pointer += 2
        dprint(tag_len)
        content += ' '
        tag = word[length - (length - pointer):length - (length - pointer) + tag_len]
        content += tag + TAG_BR
        pointer += tag_len

        if pointer > length:
          loooooooseeeer = "loooooooseeeer"
          self.view.show_popup(loooooooseeeer, on_navigate=self.navigate)
          return
      # while 
      
      # for letter in self.word :
        # content = content + (str(odd/2+.5)[:1] if odd % 2 else '')
        # content = content + ' ' + bin(int(letter, 16))[2:].zfill(4) 
        # content += letter + TAG_BR
      # for

      link = '<a href="' + re.sub(TAG_BR,NEW_LINE,content) + '">copy me</a>'
      content += link

      self.view.show_popup(content, on_navigate=self.navigate)
      return

    def parseBpcAddldata(self):
      dprint("parseBpcAddldata: 1")
      if self.check_hex() != 1:
        return
      # if

      content = ''
      word = self.word
      length = len(word)
      pointer = 0
      dprint(length)
      if length %2 == 1:
        print("odd senses!")
        return
      # if
      while pointer != length:
        tag_id = word[length - (length - pointer):length - (length - pointer) + 2]
        pointer += 2
        if ( (int(tag_id,16) & 0x80) == 0x80 ):
          dprint("double tag")
          tag_id += word[length - (length - pointer):length - (length - pointer) + 2]
          pointer += 2
        # if
        dprint(tag_id)
        content += tag_id.ljust(5)

        # tag length
        tag_len_txt = word[length - (length - pointer):length - (length - pointer) + 2]
        pointer += 2

        if ( (int(tag_len_txt,16) & 0x80 ) == 0x80):
          dprint("double length")
          tag_len_txt += word[length - (length - pointer):length - (length - pointer) + 2]
          pointer += 2
          tag_len = int(tag_len_txt[1:], 16) * 2
          dprint(tag_len_txt)
        else:
          tag_len = int(tag_len_txt, 16) * 2
        # if

        content += tag_len_txt[-3:].ljust(5)

        content += ' '
        tag = word[length - (length - pointer):length - (length - pointer) + tag_len]
        content += tag + TAG_BR
        pointer += tag_len

        if pointer > length:
          dprint(content)
          loooooooseeeer = "loooooooseeeer"
          self.view.show_popup(loooooooseeeer, on_navigate=self.navigate)
          return
      # while 
      
      # for letter in self.word :
        # content = content + (str(odd/2+.5)[:1] if odd % 2 else '')
        # content = content + ' ' + bin(int(letter, 16))[2:].zfill(4) 
        # content += letter + TAG_BR
      # for

      link = '<a href="' + re.sub(TAG_BR,NEW_LINE,content) + '">copy me</a>'
      content += link

      self.view.show_popup(content, on_navigate=self.navigate)
      return


    def parsePDS(self):
      dprint("parsePDS: 1")
      # if self.check_hex() != 1:
        # return
      # if
      content = ''
      word = self.word
      length = len(word)
      pointer = 0
      dprint(length)

      while pointer != length:
        tag_id = word[length - (length - pointer):length - (length - pointer) + 2]
        content += str(tag_id) + " "
        pointer += 2

        tag_len = word[length - (length - pointer):length - (length - pointer) + 2]
        content += str(tag_len) + " "
        pointer += 2
        dprint(tag_len)
        tag = word[length - (length - pointer):length - (length - pointer) + int(tag_len, 10)]
        content += tag + TAG_BR
        pointer += int(tag_len, 10)

        if pointer > length:
          loooooooseeeer = "loooooooseeeer"
          self.view.show_popup(loooooooseeeer, on_navigate=self.navigate)
          return
      # while 
      
      link = '<a href="' + re.sub(TAG_BR,NEW_LINE,content) + '">copy me</a>'
      content += link

      self.view.show_popup(content, on_navigate=self.navigate, max_width=1000, max_height=1000)
      return

    def parsePDC(self):
      dprint("parsePDC")
      content = ''
      i = -1
      for letter in self.word:
        i += 1
        if i > len(pos_data_code) - 1:
          break
        # if
        for record in pos_data_code[i]:
          if letter == record.key:
            content += record.description + " {" + record.value + "}"  + TAG_BR
          # if
        # for
      # for

      link = '<a href="' + re.sub(TAG_BR,NEW_LINE,content) + '">copy me</a>'
      content += link

      self.view.show_popup(content, on_navigate=self.navigate, max_width=1000, max_height=1000)
      return

    def parsePDC2(self):
      dprint("parsePDC")
      content = ''
      i = -1
      for letter in self.word:
        i += 1
        if i > len(pos_data_code) - 1:
          break
        # if
        
        # cardholderAuthenticationCapability        
        dprint([ k for k,v in globals().items() if v is pos_data_code[1]][0])

        content += [ k for k,v in globals().items() if v is pos_data_code[i]][0] + " (" + str(i+1) + ")" + NEW_LINE
        content += TAG_UL_A + NEW_LINE

        for record in pos_data_code[i]:
          if letter == record.key:
            content += TAG_LI_A + TAG_I_A + TAG_U_A + record.key + " " + record.description + " {" + record.value + "}"  + TAG_U_Z + TAG_I_Z + TAG_LI_Z 
          else:
            content += TAG_LI_A + record.key + " " + record.description + " {" + record.value + "}"  + TAG_LI_Z 
          # if
        # for
        content += TAG_UL_Z + NEW_LINE
      # for

      link = '<a href="' + re.sub(TAG_BR,NEW_LINE,content) + '">copy me</a>'
      content += link

      self.view.show_popup(content, on_navigate=self.navigate, max_width=1000, max_height=1000)
      return


    def parseString(self, filename, min_length, max_length):
      dprint("parseString")
      content = ''
      counter = 0

      word = self.word 

      m = re.split(NEW_LINE, sublime.load_resource(filename))
      dprint(len(m))
      
      if len(m) <= 0:
        self.view.show_popup('file not found', on_navigate=self.navigate)
        return
      # if

      for bit in word:
        if counter > len(m) - 1:
          break
        # if

        if counter % 8 == 0:
          content += TAG_UL_A + NEW_LINE
        # if

        if bit == '1':
          content += TAG_LI_A + TAG_U_A + TAG_I_A + '1 ' + m[counter] + TAG_I_Z + TAG_U_Z + TAG_LI_Z + NEW_LINE
        elif bit == '0':
          content += TAG_LI_A + '0 ' + m[counter] + TAG_LI_Z + NEW_LINE
        else:
          self.view.show_popup("We must not be here.")
          return
        # if

        counter += 1
        if counter % 8 == 0:
          content += TAG_UL_Z + NEW_LINE
        # if
      # for 

      dprint(content)

      self.view.show_popup(content, max_width=1000, max_height=1000)
      return

    def testHTML(self):
      dprint("testHTML")
      content = sublime.load_resource("Packages/User/test.html")
      self.view.show_popup(content)
      return

    def parseDisableStatus(self):
      dprint("parseDisableStatus")
      return

    def hide_popup(self):
      self.view.window().run_command('hide_popup')

    def navigate(self, href):
      # self.add_to_clip_board_win(href)
      sublime.set_clipboard(href)
      self.hide_popup()

    def add_to_clip_board_win(self, text):
      command = 'echo ' + text.strip() + '| clip '
      os.system(command)

    def run(self, edit):
      v=self.view;

# already selected
      word = v.substr(v.sel()[-1])

# owervise try to select something
      if re.match("^$",word):
        v.window().run_command('find_under_expand')
        word = v.substr(v.sel()[-1])
      # if

# remove dots and spaces from goal string
      if re.search("[. ]",word):
        word = re.sub('[. ]','',word)
      # if

# slight check of selected area
      if re.match("^$",word):
        content = 'empty selection'
        v.show_popup(content)
        return
      else:
        self.word = word
# append only those items which has appropriate length
        items = []

        if len(word) == TVR_LEN:
          dprint("TVR_LEN!")
        # if
        
        items.append('default')
        items.append('TVR')
        items.append('TSI')
        items.append('disab_stat')
        items.append('warn_stat')
        items.append('hw_config')
        items.append('EMV TLV')
        items.append('bpc_addldata')
        items.append('CVR (Visa-VIS)')
        items.append('CVR (Visa-CCD)')
        items.append('CVR (MasterCard)')
        items.append('pos data code')
        items.append('PDS')
        items.append('curr_trans header flags')
        items.append('D5 application control mchip')
        items.append('biciso flags')
        if DEBUG == 1:
          items.append('test HTML')
          dprint(items)
        # if 

# show "how to parse window"
        sublime.active_window().show_quick_panel(items, on_select=self.on_choice_function)
      # if-elif-else

# order is important
    def on_choice_function(self, index):
      dprint("index = %d" % index)

      if   index == 0:
        self.parseDef()
      elif index == 1:
        self.parseTag(FILE_TVR   , TVR_LEN, TVR_LEN)
      elif index == 2:
        self.parseTag(FILE_TSI   , TSI_LEN, TSI_LEN)
      elif index == 3:
        self.parseTag(FILE_DISAB ,       1,      16)
      elif index == 4:
        self.parseTag(FILE_WARN  ,       1,      16)
      elif index == 5:
        self.parseTag(FILE_CONFIG,       1,      16)
      elif index == 6:
        self.parseTLV()
      elif index == 7:
        self.parseBpcAddldata()
      elif index == 8:
        # self.parseCVRVisa()
        self.parseTag(FILE_CVR_VI_VIS, 12, 12)
      elif index == 9:
        # self.parseCVRVisa()
        self.parseTag(FILE_CVR_VI_CCD, 12, 12)
      elif index == 10:
        # self.parseCVRMaster(FILE_CVR_MC, 1, 24)
        self.parseTag(FILE_CVR_MC   , 12, 12)
      elif index == 11:
        self.parsePDC2()
      elif index == 12:
        self.parsePDS()
      elif index == 13:
        self.parseTag(FILE_HEADER, 1, 160)
      elif index == 14:
        self.parseTag(FILE_D5, D5_LEN, D5_LEN)
      elif index == 15:
        self.parseString(FILE_BICISO_FLAGS, BICISO_FLAGS_LEN, BICISO_FLAGS_LEN)
      elif index == 16:
        self.testHTML()
      else:
        self.done()
      # if-elif-...-elif-else