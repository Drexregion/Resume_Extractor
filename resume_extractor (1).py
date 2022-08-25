#!/usr/bin/env python
# coding: utf-8

# In[96]:


import spacy #nlp
import pdfminer
import re
import os
import pandas as pd


# In[97]:


import pdf2txt


# In[98]:


# converting pdf to text


# In[99]:


def convert_pdf(f):
    output_name = os.path.basename(os.path.splitext(f)[0]) + '.txt'
    output_filepath = os.path.join("output/text/",output_name)
    pdf2txt.main(args=[f,"--outfile",output_filepath])#saves in the given location
    print(f"{output_filepath} saved successfully !!!")
    return open(output_filepath, encoding="utf8").read()


# In[100]:


# loading the language model


# In[101]:


nlp = spacy.load('en_core_web_sm')


# In[102]:


# ----------place holders--------------
result_dict = {"name":[],"phone":[],"email": [],'skill':[]}
names = []
phones = []
emails = []
skills = []


# In[103]:


#  ----------functionality-------------------
def pdf_parser(text):
    skill_set = re.compile('python|sql|tableau|java|hadoop')
    phone_no = re.compile('\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}')
    doc = nlp(text)
    print('STARTING EXTRACTION!!!!!')
    name = [entity.text for entity in doc.ents if entity.label_ == 'PERSON'][0]
    email = [entity for entity in doc if entity.like_email == True ][0]
    phone = re.findall(phone_no , text.lower())
    skill = re.findall(skill_set, text.lower())
    unique_skill = str(set(skill))
    names.append(name)
    emails.append(email)
    phones.append(phone)
    skills.append(unique_skill)
    print('EXTRACTION COMPLETE!!!!!!!')


# In[104]:


for file in os.listdir('resumes/'):
    if file.endswith('.pdf'):
        print('Reading..........' , file)
        txt = convert_pdf(os.path.join('resumes/',file))
        pdf_parser(txt)


# In[106]:


result_dict['name'] = names
result_dict['phone'] = phones
result_dict['email']= emails
result_dict['skill'] = skills


# In[108]:


result_dataframe = pd.DataFrame(result_dict)


# In[110]:


result_dataframe.to_csv('output\csv\parsed_resumes.csv')


# In[ ]:




