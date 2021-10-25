# input_processor.py

# Starter code for assignment 1 in ICS 32 Programming with Software
# Libraries in Python

# Replace the following placeholders with your information.

# Hayden Powers
# powersh@uci.edu
# 56169764


from pathlib import Path
import sys
import os
from Profile import Profile, Post, DsuFileError, DsuProfileError


# Global user profile to access contents of current Profile object
current_user = Profile()
current_path = ''


# r_option will output a directory content recursively
def r_option(path):
    directories, contents = [], []

    for p in path.iterdir():            
        if p.is_file():                   
            contents.append(p)           
        elif p.is_dir():
            directories.append(p)        

    if(len(directories) != 0):           
        for d in directories:
            contents.append(d)                  
            contents.extend(r_option(Path(d)))  

    return contents


# f_option will output only files given , excluding directories
def f_option(contents, query):
    file_contents = []

    if(len(contents) == 0): # -r was not called
        files, directories, contents = l_command(query)
        return files
    else:
        for c in contents:
            if Path(c).is_file():
                file_contents.append(c)

    return file_contents


# s_option will output only files that match a given file name
def s_option(contents, query):
    file_matches = []
    input2 = query[3]

    if(len(contents) == 0): # -r was not called
        files, directories, contents = l_command(query)
    
    for c in contents:
        if Path(c).name == input2[1:]:
            file_matches.append(c)

    return file_matches


# e_option will output oly files that match a given file extension
def e_option(contents, query):
    suffix_matches = []
    input2 = query[3]
    input2 = input2[1:] # to get rid of first "/"
    
    if(input2[0] != "."):
        input2 = "."+input2 

    if(len(contents) == 0): # -r was not called
        files, directories, contents = l_command(query)

    for c in contents:
        if Path(c).suffix == input2:
            suffix_matches.append(c)

    return suffix_matches


# n_option specifies the name to be used for a new file
def n_option(query):
    if(query[0] != 'C'):
        return
    filename = query[3]
    filename = filename[1:]+".dsu"
    return filename
    

# options() will be the method that will moderate option calls
# will pass around a list of contents to refine based on
# what is called
def options(query):
    given_options, input2 = query[2], query[3]
    contents = []
    r, f, s, e, n = False, False, False, False, False
    
    for o in given_options:
        if o == "-r":
            r = True     
        if o == "-f":
            f = True   
        if o == "-s":
            s = True
        if o == "-e":
            e = True
        if o == "-n":
            n = True

    # Some checks/conditions for joining options together
    if(n and query[0] !='C' and (input2 == '/' or input2 == '')):
        error()
        return
    elif((s or e or n) and (input2 == '/' or input2 == '')):
        error()
        return
    elif((r or f or s or e) and query[0] != 'L'):
        error()
        return

    # Check which options are given
    if r:
        contents = r_option(query[1]) # -r JUST given path
    if f:
        contents = f_option(contents, query)
    if s:
        contents = s_option(contents, query)
    if e:
        contents = e_option(contents, query)

    # Print final contents
    for c in contents:
        print(c)


# user option deals with printing or editing username of current_profile
def usr_option(query, command, string):
    global current_user, current_path
    if command == "E":
        # Edit username
        current_user.username = string
        try:
            current_user.save_profile(current_path)
            print("Current username: ", current_user.username)
        except DsuFileError as e:
            print(e)

    else: # Print username
        print("Current username: ", current_user.username)


# pwd option will either print or edit the password of current_profile
def pwd_option(query, command, string):
    global current_user, current_path
    if command == "E":
        # Edit password
        current_user.password = string
        try:
            current_user.save_profile(current_path)
            print("Current username: ", current_user.password)
        except DsuFileError as e:
            print(e)

    else: # Print username
        print("Current password: ", current_user.password)


# bio option will print or edit the bio of current_profile
def bio_option(query, command, string):
    global current_user, current_path
    if command == "E":
        # Edit password
        current_user.bio = string

        try:
            current_user.save_profile(current_path)
            print("Current bio: ", current_user.bio)
        except DsuFileError as e:
            print(e)

    else: # Print username
        print("Current bio: ", current_user.bio)


# addpost only accepts E command, will edit a post based on string param
def addpost_option(query, string):
    global current_user, current_path
    current_user.add_post(string)

    try:
        current_user.save_profile(current_path)
        print(f"Added post: {string}")
    except DsuFileError as e:
        print(e)


# delpost only accepts E command, will delete a post based on string index
def delpost_option(query, string):
    global current_user, current_path

    try:
        current_user.del_post(int(string)) # NEED TO TEST FOR INT VALUE
        current_user.save_profile(current_path)
        print(f"Deleted post: {string}")
    except DsuFileError as e:
        print(e)
    except TypeError:
        print("\nInvalid index of entry - please enter only number value.")



# posts only accepts P command, will print all posts 
def posts_option(query):
    global current_user
    posts = current_user.get_posts()
    for p in posts:
        print(posts.index(p), ": ", p)


# posts only accept P command, will print post at string index
def post_option(query, index):
    global current_user
    posts = current_user.get_posts()
    try:
        print(index, ": ", posts[index])
    except IndexError:
        error()
        return
    

# all only accepts P command, will print everything in profile object
def all_option(query):
    global current_user
    print("\nUsername: ", current_user.username)
    print("Password: ", current_user.password)
    print("Bio: ", current_user.bio)
    posts_option(query)


# Responsible for making changes to Profile posts
# ASSUMES QUERY IS VALID AND ACCURATE - CHECKS DONE IN VALIDATE_PROFILE
def profile_options(query):
    global current_user, current_path
    command = query[0]

    for e in query:
        if e == "-usr":
            if command == "P":
                usr_option(query, command, "")
            else:
                string = query[query.index(e) + 1]
                usr_option(query, command, string) # Can call methods from here

        if e == "-pwd":
            if command == "P":
                pwd_option(query, command, "")
            else:
                string = query[query.index(e) + 1]
                pwd_option(query, command, string)
            
        if e == "-bio":
            if command == "P":
                bio_option(query, command, "")
            else:
                string = query[query.index(e) + 1]
                bio_option(query, command, string)
            
        if e == "-addpost":
            if len(query) < 3: 
                error()
                return
         
            string = query[query.index(e) + 1]
            addpost_option(query, Post(entry=string))
            
        if e == "-delpost":
            if len(query) < 3: 
                error()
                return
            
            string = query[query.index(e) + 1]
            delpost_option(query, string)
            
        if e == "-posts": 
            posts_option(query)
            
        if e == "-post":
            if len(query) < 3: 
                error()
                return
            
            string = query[query.index(e) + 1]
            post_option(query, int(string))
            
        if e == "-all":
            all_option(query)



# O command opens an existing .dsu file 
def o_command(query):
    global current_user, current_path
    current_path = query[1]
    if(current_path.suffix != '.dsu'):
        error()
        return
    else:
        try:
            current_user.load_profile(query[1]) 
            print("Profile loaded for: ", f"{current_user.username}")
        except (DsuFileError, DsuProfileError) as e:
            print("Profile does not exist!")


# R command reads contents of a file
def r_command(query):
    global current_user, current_path
    current_path = path = query[1]
    
    if(path.suffix != '.dsu'):          
        error()
        return
    else:
        if(os.path.getsize(path) == 0):               
            print("EMPTY")             
        else:                                   
            try:
                print(path.read_text())         
            except FileNotFoundError as fnfe:
                error()
                return


# D command will delete the file that the path is pointing to
def d_command(query):
    path = query[1]
    if(Path(path).suffix != '.dsu'):            # Checks for .dsu suffix
        error()
        return
    else:
        path.unlink()                           # Deletes if .dsu
        
    print(str(path), "DELETED")        


# C command will create a new file in the specified directory and
# update global current_path
def c_command(query):
    global current_path
    path = query[1]
    usrnm = input("Username: ")
    pw = input("Password: ")

    if usrnm == '' or pw == '':
        c_command(query)

    current_user.username = usrnm
    current_user.password = pw
    
    filename = n_option(query)                  # Get filename from -n
    current_path = Path(path).joinpath(filename)
    Path(current_path).touch()                  # Create file at path location

    try:
        current_user.save_profile(current_path)
    except DsuFileError as e:
        print(e)

    
    print(str(current_path))                        # Print the new path to file
        

# L command will list the contents of the user specified directory
def l_command(query):
    files, directories, contents = [], [], []
    for p in query[1].iterdir():
        if(p.is_file()):     
            files.append(p)
        elif(p.is_dir()):
            directories.append(p)

    contents.extend(files)
    contents.extend(directories)
    
    return files, directories, contents


# command will be the method that will take care of moderating
# which commands to call based on query[0]
def command(query):
    cmd = query[0]
    contents = []
    
    if(cmd == 'L'):
        files, directories, contents = l_command(query)

        if(len(query[2]) == 0): # If options don't exist, just list contents
            for c in contents:
                print(c)
                
    elif(cmd == 'C'):
        c_command(query)      
    elif(cmd == 'D'):
        d_command(query)
    elif(cmd == 'R'):
        r_command(query)
    elif(cmd == 'O'):
        o_command(query)

        
# Processes user input by using parse() and validate()
# then it calls command() and/or option() to process
# user's query
def process_input(user_input) -> list:
    input_parts = []
    l = len(user_input)

    # Process string from RIGHT to LEFT
    for i in range(0, l-1):
        segment = user_input[(l-i)-4:l-i]
        if(segment != ''):
            input_parts.append(segment)

    query = parse(input_parts, user_input)

    # check if profile commands before file system commands
    if query[0] == 'E' or query[0] == 'P':

        if(validate_profile(query)):
            # Call special profile_options to dea with request
            profile_options(query)
            return
        else:
            error()
            return
            
    valid = validate(query)

    if(valid):
        #print("Input valid")
        if(len(query[2]) != 0):  # Checks if options exists first
            options(query)       # If they do, call options() FIRST
        command(query)           # Calls command SECOND
        return
    else:
        error()
        return
    

# Takes the query generated by parse and validates
# each component. Including if path exists.
# If valid, returns TRUE, if not, returns FALSE
def validate(query) -> bool:
    
    #print("QUERY: ", query) 
    commands = ['L', 'C', 'D', 'R', 'O']
    options = ['-r', '-f', '-s', '-e', '-n', '']
    path = query[1]

    # Check commands first
    if(query[0] not in commands):
        return False
    if(query[0] in commands and query[1] == ''):
        return False
    if(query[0] == 'C' and ('-n' not in query[2] or query[3] == '')):
        return False

    # Check if options exist and are valid
    if(len(query[2]) != 0):
        options_valid = False
        for o in query[2]:
            if o in options:
                options_valid = True
                
        if options_valid == False:
            return False    
    
    # Check is path exists
    if(Path(path).exists() == False):
        return False
    
    return True


# Validates E and P queries
def validate_profile(query):
    global current_user, current_path
    valid = True
    options = ['-usr', '-pwd', '-bio', '-addpost', '-delpost',
               '-posts', '-post', '-all']

    # Check to see if we even have an existing profile
    if(current_user.username == None or current_path == ' '):
        return False
    
    # check to see if second element is even an option
    if(query[1] not in options):
        return False
    
    for o in options:
        if o in query: # Check to see if the options even exist

           # Only E command can be used with -addpost and -delpost
            if (query[0] == "P" and (o == options[3] or o == options[4])):
                valid = False
           # Only P command can be used with -posts, -post, and -all
            elif (query[0] == "E" and (o == options[5] or o == options[6]
                                     or o == options[7])):
                valid = False
            
           # -all should be standalone
            elif (len(query) > 2 and o == options[7]):
                valid = False
            else:
                valid = True
        
    return valid
    
    
# NEW a2 ADDITION - does not need Path to work
def parse_profile(input_parts, user_input, command):
    #global current_user
    query, options, strings = [command], [], [] # Add command passed in from parse()
    string, option = '', ''
    quotes_toggle = False

    for char in user_input:
        # Toggle quotes to gather strings
        if char == "\"" and quotes_toggle == False:
            quotes_toggle = True
        elif char == "\"" and quotes_toggle == True:
            quotes_toggle = False
        
        if quotes_toggle == True:
            string = string + char
        else:
            if string != '':
                strings.append(string.replace("\"", ''))
                string = '' # reset string until toggle is on again

        # Find options while toggle is off, skip command
        if quotes_toggle == False and char != user_input[0]:
            if char == ' ':
                if option != '' and option != "\"":
                    options.append(option)
                option = ''
            else:
                option = option + char
                
    # Add all to single query to return for use
    for i in range(len(options)):
        query.append(options[i])
        if len(strings) == len(options):
            query.append(strings[i])
        
    #print("QUERY: ", query)
    return query


# Parses the input into a query to ensure it holds format:
# [COMMAND] [INPUT] [[-]OPTION] [INPUT]
def parse(input_parts: list, user_input: str):
    index_before_path = 0
    command, input2, path,  = '', '', ''
    r, f, s, e, n = False, False, False, False, False
    options, query = [], []
    
    for seg in input_parts:
        #print("SEG: ", seg)
        # Check for L, C, D, R, and Q commands
        if(seg == input_parts[-1]):
            if(seg[0] == 'L'):
                command = 'L'
            elif(seg[0] == 'C'):
                command = 'C'
            elif(seg[0] == 'D'):
                command = 'D'
            elif(seg[0] == 'R'):
                command = 'R'
            elif(seg[0] == 'O'):
                command = 'O'
            elif(seg[0] == 'E'):
                command = 'E'
            elif(seg[0] == 'P'):
                command = 'P'
            elif(seg[0] == 'Q'):
                sys.exit()

        # NEW ADDITION - FOR E AND P COMMANDS 
        if(command == 'E' or command == 'P'):
            query = parse_profile(input_parts, user_input, command)
            return query
            
        # Check for second input (filenames, suffixes, etc)
        # If all options are false, then this is BEFORE any
        # options are found in input_parts
        if(r == False and f == False and s == False and e == False and n == False):
            if("/" not in seg or "-r " not in seg or "-f " not in seg
               or "-n " not in seg or "-s " not in seg or "-e " not in seg):
                input2 = input2 + seg[-1]
                
        # Check for -r, -f, -s, -e options
        if(' -r ' in seg and r == False):
            r = True
            options.append("-r")
        elif(' -f ' in seg and f == False):
            f = True
            options.append("-f")
        elif(' -s ' in seg and s == False):
            s = True
            options.append("-s")
        elif(' -e ' in seg and e == False):
            e = True
            options.append("-e")
        elif(' -n ' in seg and n == False):
            n = True
            options.append("-n")

    # Get index of last option in input_parts to know where
    # to look in list for path in input_parts
    if(len(options) != 0):
        index_before_path = input_parts.index(' '+options[-1]+' ')+3
        
        # Separate for loop to get path
        for seg in input_parts[index_before_path:]:
            path = path + seg[-2]
    else:
        path = input2+"/"               # If no options, path was recorded in input2


    # INPUT REFINEMENTS:
    path = path[::-1]                   # Reversing path, since it's backwards
    input2 = "/"+input2[::-1].strip()
    for o in ['-r', '-f', '-s', '-e', '-n']:    # Making sure no options got caught in
        if input2[:2] == o:                     # the front of input2 by mistake
            input2 = input2.replace(o, "")      # If so, replace with ''
            
    # Store parsed values in query list
    query.append(command)               
    if(path == ' '):                    
        query.append('')                
    else:
        query.append(Path(path.strip()))    
    query.append(options)                   
    query.append(input2.strip())            

    # Last refinements of query 
    if(str(query[1]) == query[3]):      
        query.remove(query[3])          
        query.insert(3,'')              
                                        
    if(query[3] == '/'):            
        query[3] = ''                   # If input2 is just a /, that means its empty
                                        
    return query


# This method will simply update the profile of current_user to another user
def update_profile(profile: Profile, path):
    global current_user, current_path
    current_path = path
    current_user = profile


# Call this for all areas that require an error message
def error():
    print("ERROR")


# Start loop
#while True:
#    if __name__ == '__main__':
#        user_input = input()
#        if(user_input == ''):
#            continue
#        process_input(user_input+" ")

    
