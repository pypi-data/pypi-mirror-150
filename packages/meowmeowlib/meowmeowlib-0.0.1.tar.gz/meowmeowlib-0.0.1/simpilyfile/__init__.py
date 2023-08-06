import os

# reads first n lines
def readnline(filename,no_of_lines):
    f = open(filename,'r')
    data = ""
    for i in range(no_of_lines):
        data += f.readline()
    f.close()
    return data

# reads lines from between
def readanyline(filename,start_line,end_line = -1):
    f = open(filename,'r')
    data = ""
    for i in range(start_line - 1):
        f.readline()
    if end_line == -1:
        data = f.read()
        return data
    else :
      for i in range(end_line - start_line + 1):
          data += f.readline()
    f.close()
    print(end_line)
    return data

#appends to file
def append(filename,string):
    a = filename
    f = open(a,'a')
    f.write(string)
    f.close()

# appends lines to file
def appendline(filename,string):
    a = filename
    f = open(a,'r')
    data = ""
    data = f.read()
    f = open(a,'w')
    if data == "":
      temp = string
      f.write(temp)
      f.close()
    else:
      temp = data + '\n' + string
      f.write(temp)
      f.close()

# Creats new file
def newfile(filename):
    a = filename
    f = open(a,'w')
    f.close()

# Splits even and odd numbers into different files
def numsplit(filename):
    f = open(filename,'r')
    data = f.read()
    l1,l2,l3 = [],[],[]
    if ('\n' in data):
        l1 = data.split('\n')
    elif (','in data):
        l2 = data.split(',')
    elif(' 'in data):
        l3 = data.split(' ')
    f.close()
    l = l1+l2+l3
    listlen = len(l)
    if os.path.exists("even.txt"):
        os.remove("even.txt")
    if os.path.exists("odd.txt"):
        os.remove("odd.txt")
    fe = open('even.txt','a')
    fo = open('odd.txt','a')
    for i in l:
        x = int(i)
        x = x%2
        if x == 0:
            fe.write(i+'\n')
        else:
            fo.write(i+'\n')
    fe.close()
    fo.close()

# Counts the number of lines, words and characters in a file
def count(filename):
    f = open(filename,'r')
    data = f.read()
    line = 0
    words = 0
    chars = 0
    l1 = 0
    l2 = []
    if ('\n' in data):
        l1 = data.split('\n')
        line = len(l1)        
    for i in l1:
        temp = i.split(" ")
        l2 = l2 + temp
    f.close()
    words = len(l2)
    while '\n' in data:
      data = data.replace('\n',"")
    chars = len(data)
    l = [line,words,chars]
    return l

# Append List 
def appendlist(filename,List,ender = ' '):
    a = filename
    f = open(a,'a')
    l = List
    for i in l:
        x = str(i)
        f.write(x + ender)
    f.close()
# Writes a list to the string
def writelist(filename,List,ender = ' '):
    a = filename
    f = open(a,'w')
    f.write("")
    f.close()
    f = open(a,'a')
    l = List
    for i in l:
        x = str(i)
        f.write(x + ender)
    f.close()
# inserting in between file
def insert(filename,position,string):
    f = open(filename,'r')
    data = f.read()
    f.close()
    temp = data[:position] + string + data[position]
    f = open(filename,"w")
    f.write(temp)
    f.close()

# read file from between
def readfrom(filename,position):
    f = open(filename,'r')
    f.seek(position)
    data = f.read()
    f.close()
    return data
# clears file
def clear(filename):
  f = open(filename,'w')
  f.write('')
  f.close()
# fib series
def fib(n):
    e1 = 0
    e2 = 1
    e3 = 0
    i = 2
    if n == 1:
        return 0
    if n == 2:
        return 1
    while i<n:
        e3 = e1 + e2
        e1 = e2
        e2 = e3
        i += 1
    return e3
# Sum of first n natural numbers
def nsum(n):
  s = n*(n+1)
  s = s/2
  return s
# sum of first n odd numbers
def oddnsum(n):
  return n*n
# sum of first n even numbers
def evensum(n):
  return n*(n+1)
# replaces a character with another
def replace(filename,char,new_char,display = 0):
  f = open(filename,'r')
  data = f.read()
  if char in data:
    data = data.replace(char,new_char)
  f.close()
  f = open(filename,'w')
  f.write(data)
  f.close()
  if display != 0:
    return data

#counts the occurance of a character
def occur(filename,char):
  if type(char) != str:
    raise TypeError(f"Function expected character --> recieved {type(char)}???")
  if len(char) > 1:
   raise TypeError(f"Function expected character --> recieved {type(char)}???")
  f = open(filename,'r')
  count = 0
  data = f.read()
  before = len(data)
  if char in data:
    data = data.replace(char,"")
  after = len(data)
  return before-after

# saparate everychar by a given symbol
def symsep(filename,char,display = 0):
  if type(char) != str:
    raise TypeError(f"Function expected character --> recieved {type(char)}???")
  if len(char) > 1:
   raise TypeError(f"Function expected character --> recieved {type(char)}???")
   f = open(filename,'r')
   data = f.read()
   f.close()
   f = open(filename,'w')
   temp = ""
   for i in data:
     temp += i
   f.write(temp)
   if display != 0:
    return temp

# Words ending with
def word_count_endwith(filename,char):
   if type(char) != str:
    raise TypeError(f"Function expected character --> recieved {type(char)}???")
   if len(char) > 1:
    raise TypeError(f"Function expected character --> recieved {type(char)}???")
   f = open(filename,'r')
   data = f.read()
   l1,l2 = [],[]
   count = 0
   if ('\n' in data):
        l1 = data.split('\n')
        line = len(l1)        
   for i in l1:
        temp = i.split(" ")
        l2 = l2 + temp
   for i in l2:
     if i[-1] == char:
       count += 1
   f.close()
   return count

# display words less than n characters
def wordsized(filename,size_of_word):
  if type(size_of_word) != int:
    raise TypeError(f"Function expected int --> recieves {type(size_of_word)}???")
  f = open(filename,'r')
  data = f.read()
  l1,l2 = [],[]
  count = []
  if ('\n' in data):
        l1 = data.split('\n')
        line = len(l1)        
  for i in l1:
        temp = i.split(" ")
        l2 = l2 + temp
  for i in l2:
      if len(i) == size_of_word:
        count.append(i)
  return count
# gives info of the aurthor
def credits_to():
    print("This package was developed by Surya Teja Pallapu")
    print('On 12-05-2022')
    print('Just For Fun')
    print("Because He was getting bored ~_~")
#non sense
def roll():
    print("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
