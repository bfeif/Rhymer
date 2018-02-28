
#!/usr/bin/env python
import web
from web import form
import scipy.io as sio
import h5py
import random

from pyflann import *
from numpy import *

web.config.debug=False
render = web.template.render('C:\\Anaconda2\\templates\\')
urls = (
    '/sum', 'get_sum',
    '/analogy', 'get_analogy',
    '/poem', 'get_poem',
    '/acrostic','get_acrostic',
    '/','get_homepage',
    '/rhyme','get_rhyme'
)

app = web.application(urls, globals())

#mat = sio.loadmat('C:\matlab apps\cyc\word.mat')
#obj_cells = mat['word']
mat = sio.loadmat('C:\matlab apps\cyc\cleanword.mat', struct_as_record=False, squeeze_me=True)
cells = mat['word']
enumerated=list(enumerate(cells))
def getKey(item):
  return item[1]
alphabetized_words = sorted(enumerated, key=getKey)
#ab_index, ab_words_numpy = zip(*alphabetized_words)
def tostring(item):
  return (item[0], str(item[1]))
ab_words = map(tostring,alphabetized_words)
del alphabetized_words
del enumerated

rhymeword_mat = sio.loadmat('C:\\matlab apps\\cyc\\rhymepair.mat', struct_as_record=False, squeeze_me=True)
rhymeword_cells=rhymeword_mat['rhymepair']



mat_contents = h5py.File('C:\matlab apps\cyc\h3.mat','r')
item_name = '/h3'
data = mat_contents.get(item_name)
np_data64 = array(data)
np_data = np_data64.astype(float32)
rhymepair_mat = h5py.File('C:\\matlab apps\\cyc\\rhymepairh3.mat','r')
item_name = '/rhymepairh3'
data = rhymepair_mat.get(item_name)
data64=array(data)
rhyme_dataset=data64.astype(float32)
flann = FLANN()
del data
del data64
del np_data64


class get_sum:
    def GET(self):
     i = web.input(ita="none",itb="none")
     output = ' ';
     arr_index1 = where(cells == i.ita)[0][0]
     arr_index2 = where(cells == i.itb)[0][0]
     
     testset = np_data[arr_index1,:]+np_data[arr_index2,:]
     result,dists = flann.nn(np_data,testset,25,algorithm="linear")
     for ii in xrange(0,24):
       output += str(cells[result[0]][ii])
       output += ' ';
     return output

class get_analogy:
    def GET(self):
     i = web.input(ita="none",itb="none",itc="none")
     output = ' ';
     arr_index1 = where(cells == i.ita)[0][0]
     arr_index2 = where(cells == i.itb)[0][0]
     arr_index3 = where(cells == i.itc)[0][0]
     
     testset = np_data[arr_index2,:]+np_data[arr_index3,:]-np_data[arr_index1,:]
     result,dists = flann.nn(np_data,testset,25,algorithm="linear")
     for ii in xrange(0,24):
       output += str(cells[result[0]][ii])
       output += ' ';
     return output

class get_poem:
    def GET(self):
     i = web.input(ita="none",itb="none")
     output = ' ';
     arr_index2 = where(cells == i.itb)[0][0]
     testset = np_data[arr_index2,:]
     word_generator = (w for w in ab_words if w[1].startswith(i.ita))
     constrained_list = list(word_generator)
     constrained_index, constrained_words  = zip(*constrained_list)
     constrained_np=np_data[constrained_index,:]
     result,dists = flann.nn(constrained_np,testset,25,algorithm="linear")
     for ii in xrange(0,24):
       output += str(constrained_words[result[0][ii]])
       output += ' ';
     return output

class get_acrostic:
  def GET(self):
     i = web.input(ita="awesome",itb="default")
     output = 'SILLY ACROSTICS\n\n';
     location = where(cells == i.ita)
     if size(location)>0:
         arr_index2 = location[0][0]
     else:
         print 'defaulted to awesome\n'
         arr_index2 = where(cells == 'awesome')
     location = where(cells == i.itb)
     if size(location)>0:
         arr_index1 = location[0][0]
         testset = np_data[arr_index2,:]+0*np_data[arr_index1,:]
     else:
         testset = np_data[arr_index2,:]
     for letter in i.itb:
       if letter == '_':
          output+= '\n'
       else:
           word_generator = (w for w in ab_words if w[1].startswith(letter))
           constrained_list = list(word_generator)
           constrained_index, constrained_words  = zip(*constrained_list)
           constrained_np=np_data[constrained_index,:]
           result,dists = flann.nn(constrained_np,testset,25,algorithm="linear")
           output += letter.upper()
           output +=' '
           random_integer = random.randint(0, 5)
           #to do: no using the same word twice, no words matching the input words
           output += str(constrained_words[result[0][random_integer]])
           output += '\n'
     return output
class get_homepage:
  def __init__(self):
       self.registerForm = web.form.Form(
           
            web.form.Textbox('letters', web.form.notnull, description='make acrostic for this word:'),
            web.form.Textbox('theme', web.form.notnull, description='theme:'),
           
            web.form.Button('Generate!'),

       )

  def GET(self):
      form = self.registerForm()
      return render.form(form,' ')
        
  def POST(self): 
      form = self.registerForm()

      if(not form.validates()):
            return render.form(form,'')
      else:
         #return "Form successfuly sent! Username: %s, password: %s" % \
         #       (form.d.letters, form.d.theme)
     
         itb = "%s" % (form.d.letters)
         ita = "%s" % (form.d.theme)   
         print ita
         print itb
         location = where(cells == ita)
         output='<p>Results:<p><p></p>'
         if size(location)>0:
             arr_index2 = location[0][0]
         else:
             print 'defaulted to awesome\n'
             location = where(cells == "awesome")
             arr_index2 = location[0][0]
             output+='<p>I did not recognize the theme word so I used AWESOME instead.</p>'
         location = where(cells == itb)
         if size(location)>0:
             arr_index1 = location[0][0]
             testset = np_data[arr_index2,:]+0*np_data[arr_index1,:]
         else:
             testset = np_data[arr_index2,:]
         for letter in itb:
           if letter == '_':
              output+= '<p></p>'
           if letter == ' ':
              output+= '<p></p>'
           else:
               word_generator = (w for w in ab_words if w[1].startswith(letter))
               constrained_list = list(word_generator)
               constrained_index, constrained_words  = zip(*constrained_list)
               constrained_np=np_data[constrained_index,:]
               result,dists = flann.nn(constrained_np,testset,25,algorithm="linear")
               output+= '<p><strong style="font-size: 200%;">'
               output += letter.upper()
               output +='</strong>  '
               random_integer = random.randint(0, 10)
               #to do: no using the same word twice, no words matching the input words
               output += str(constrained_words[result[0][random_integer]])
               output += '</p>'
         return render.form(form,output)

class get_rhyme:
  
     def __init__(self):
       self.registerForm = web.form.Form(
           
         web.form.Textbox('term', web.form.notnull, description='find a rhyming pair similar in meaning to:'),
         web.form.Textbox('term2', description='(optional) enter another term to mix meanings:'),  
         web.form.Button('Generate!'),

       )
       
     def GET(self):
       rhymeform = self.registerForm()
       return render.rhymeform(rhymeform,' ')

     def POST(self): 
      rhymeform = self.registerForm()

      if(not rhymeform.validates()):
            return render.rhymeform(rhymeform,'')
      else:
         ita = "%s" % (rhymeform.d.term)
         itb = "%s" % (rhymeform.d.term2)
         if (ita =="sdfdsfcxvxcv") or (ita=="sxfhncvbxcvvxcv"):
           output='<p>Results:</p><p></p><div style="display:flex; flex-wrap:wrap;">'
           for ii in range(1,200):
             output += '<span style="width:20%">'
             output += 'evil evil'
             output += '</span>'
           output +='</div>'
         else:
               
             print ita
             print itb
             location = where(cells == ita)
             location2 = where(cells == itb)
             if size(location)>0:
                 arr_index1 = location[0][0]
                 testset = np_data[arr_index1,:]
                 if size(location2)>0:
                     arr_index2 = location2[0][0]
                     testset=np_data[arr_index1,:]+np_data[arr_index2,:]
                 result,dists = flann.nn(rhyme_dataset,testset,200,algorithm="linear")
                 output='<p>Results:</p><p></p><div style="display:flex; flex-wrap:wrap;">'
                 
                 count=1
                 for ii in range(1,200):
                     resultstring = str(rhymeword_cells[result[0][ii]])
                     if (ita in resultstring) or (ita.lower() in resultstring) or (itb!='' and ((itb in resultstring) or (itb.lower() in resultstring))):
                         pass
                     else:
                         output += '<span style="width:20%">'
                         output += resultstring
                         output += '</span>'
                         count=count+1
                         #output += '</p>'
                 if count<100:
                     count=1
                     result,dists = flann.nn(rhyme_dataset,testset,1000,algorithm="linear")
                     for ii in range(1,1000):
                         resultstring = str(rhymeword_cells[result[0][ii]])
                         if (ita in resultstring) or (ita.lower() in resultstring) or (itb!='' and ((itb in resultstring) or (itb.lower() in resultstring))):
                             pass
                         else:
                             output += '<span style="width:20%">'
                             output += resultstring
                             output += '</span>'
                             count=count+1
                             #output += '</p>'
                 output +='</div>'
                     
             else:
               output='<p>Sorry, word not recognized. Try a synonym?</p>'        
         return render.rhymeform(rhymeform,output)
       
if __name__ == "__main__":
    app.run()