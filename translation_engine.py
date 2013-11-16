# ----------------------------------------------------------------------------
#		* "THE BEER-WARE LICENSE" (Revision 42/023):
#		* Lukas Kawerau <coding@kawerau.org> wrote this file. As long as you retain
#		* this notice you can do whatever you want with this stuff. If we meet some day,
#		* and you think this stuff is worth it, you can buy me a beer or a coffee in return. 
#		* ----------------------------------------------------------------------------

import sys 
import os
import csv
import json
from language_codes import code_lexicon
from apiclient.discovery import build

class TranslationEngine(object):
    
    def run(self):
        self.start = Start()
        self.translator = TranslationProcess()
        self.language_picker = LanguagePicker()
        
        params = self.start.get_translation_parameters()
        converted = self.language_picker.convert_input(params[1], params[2])
        sourcefile = self.language_picker.get_source_file(converted[0])
        
        while True:
            next = self.translator.translate_file(sourcefile, params[0], 
                                                    converted[0], converted[1])
            run = next()
            
class LanguagePicker(object):
    
    def convert_input(self, base_language, target_language):
        self.base = base_language
        self.target = target_language
        
        languages = code_lexicon
        
        base_language_conv = languages.get(self.base, 'error')
        target_language_conv = languages.get(self.target, 'error')
        return base_language_conv, target_language_conv
    
    def get_source_file(self, base_language):
        self.base = base_language
        
        base_directory = os.path.dirname(os.path.abspath(__file__))
        
        short_list = os.path.join(base_directory, "languages/2000_most_frequent_words")
        sourcefile = os.path.join(short_list, "%s.csv") % self.base
        
        return sourcefile
                
    
        
class Start(object):
    
    def get_translation_parameters(self):
        
        print "Hi! Glad to see that you want to learn another language!"
        print "This script will translate a list of words of your" 
        print "target language into your native (or any other) language."
        print "What language do you want have translated?"
        
        base_language = raw_input("> ") 
        
        print "And what do you want to have it translated into?"
        
        target_language = raw_input("> ")
        
        print "Awesome!"
        print "Now, what should the file be called that you want to save"
        print "the results in?"
        
        outputfile = raw_input("> ")
        
        print "Translating now..."
        
        
        return outputfile, base_language, target_language

class TranslationProcess(object):
    
    def translate_file(self, sourcefile, outputfile, base_language, target_language):
        
        self.sourcefile = sourcefile
        self.outputfile = outputfile
        self.base_language = base_language
        self.target_language = target_language
        
        service = build('translate', 'v2',
                developerKey='YOURAPIKEYHERE')
    
        # Open a CSV file with the vocabulary in one column (one word per row)
        vocab_reader = csv.reader(open(sourcefile, 'rb'), delimiter=' ')
    
        # Create a CSV file to put the translation in
        vocab_writer = csv.writer(open(outputfile, 'w'), delimiter=',')
    
        # send each row to google and have it translated
        for row in vocab_reader:
        
            # decode each row so you can use utf-8 formatted files as input
            word = row[0].decode("utf-8")
        
            translation_object = service.translations().list(
                                source=base_language,
                                target=target_language,
                                q = word
                                ).execute()
        
            # get the translation and encode it in utf-8          
            translation = translation_object['translations'][0]['translatedText'].encode("utf-8")
            
            # write the original word and the translation to a new csv-file
            vocab_writer.writerow([row[0]]+[translation])
        
        print "Success!"
        print "Your translated file should be ready as"
        print "%s" % outputfile
        print "Have fun using these translations, but have them checked"
        print "for accuracy by a native speaker, if possible."
        print "Good bye!"
        
        exit()
