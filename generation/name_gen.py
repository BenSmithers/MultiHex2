
import os
import pickle 
import random
import numpy as np

resources_dir = os.path.join( os.path.dirname(__file__),'..','resources')

"""
Functions for generating a random name from MCMC tables! 
"""

def create_name(what, order=2, filename="Morrowind"):
    """
    The following function was written by Ross McGuyer. Credit goes to the author (currently unknown) of
    http://pcg.wikidot.com/pcg-algorithm:markov-chain, as much of the code used is derived from the example.

    create_name
    Parameter(s): what - The region type. Appended to somewhere to the returned string.
                    order - Controls how complex each look up syllable. Default value is 2.
    Return: A string to be used as a moniker for a region. Contains the region type so that users know what the region represents.
    Description: This function uses a simple markov chain to generate a name.
    """
    try:
        mid_table, start_list = open_tables(filename)
    except:
        try:
            mid_table, start_list = fill_name_tables(what, order, filename)  # The markov chain
        except:
            raise IOError("File not found! {}".format(filename))
    syns = fetch_synonyms(what)
    name = generate_name(mid_table, order, start_list)
    final_name = determine_name_style(syns, name)
    return final_name

def fill_name_tables(what, order, filename):
    """ 
    The following function was written by Ross McGuyer. Much of the credit goes to the author (currently unknown)
    of http://pcg.wikidot.com/pcg-algorithm:markov-chain, much of the code used is derived from the example.
    fill_name_table
    Parameter(s): what - The region type. Eventually used to determine the style of the generated name.
                    order - Controls how complex each look up syllable.
                    filename - the text file to read from
    Return: A table containing the markov chain and weights
    Description: This function reads from a file containing several example words/names and uses that to generate the rules for generating names.   
    """
    if not os.path.exists( os.path.join( resources_dir , 'binary_tables' )):
        os.mkdir( os.path.join( resources_dir, 'binary_tables'))

    mid_table = {}
    start_list = []
    try:
        file_obj = open(os.path.join(resources_dir, "text_files", filename), 'r')
        _file_obj = file_obj.readlines()
        file_obj.close()
    except IOError as e:
        raise IOError("I/O error({0}): {1}".format(e.errno, e.strerror))

    for word in _file_obj:
        if word[-1] == '\n':
            no_newline = word[0:len(word)-1]
        else:
            no_newline = word
        start_list.append(no_newline[:2])
        for i in range(len(no_newline) - order):
            try:
                mid_table[no_newline[i:i+order]]
            except KeyError:
                mid_table[no_newline[i:i + order]] = []
            mid_table[no_newline[i:i + order]] += no_newline[i+order]

    save_tables(start_list, mid_table, filename)

    return mid_table, start_list


def generate_name(mid_table, order, start=None, max_length=20):
    """
    The following function was written by Ross McGuyer. Much of the credit goes to the author (currently unknown)
    of http://pcg.wikidot.com/pcg-algorithm:markov-chain, since much of the code used is derived from the example.
    fill_name_table
    Parameter(s): table - The markov chain needed to form the name.
                  order - Controls how complex each look up syllable.
                  start - An index that chooses what syllable to start the new name with. Default is None, which means
                             a random syllable in table is used.
                  max_length - controls that sizes of the word. Ideally terminating characters are reached, but in rare
                                 case they are not and you don't want super long names. Default value is 20.
    Return: A string containing the a procedurally generated name.
    Description: This function splices together elements from table to create a randomized (but sensible) word or name.
    """
    name = ""

    if start == None:
        name += random.choice(list(mid_table))
    else:
        name += random.choice(start)
    try:
        while len(name) < max_length:
            if not break_name_loop(name):
                name += random.choice(mid_table[name[-order:]])
            else:
                break
    except KeyError:
        pass

    return name



def fetch_synonyms(what):
    """
    fetch_synonyms
    Parameter(s): what - The region type. Use to determine which synonym list to return.
    Return: syns - A list of strings containing synonyms of 'what'.
    Description: Takes in a string and returns a list containing the string and several synonyms.
    """
    switcher = {
        "shallows":["Bay", "Shallows"],
        "ocean":["Sea", "Ocean"],
        "prarie": ["Grasslands", "Fields", "Prairie", "Plains", "Steppes"],
        "desert": ["Desert", "Badlands", "Wastes", "Barrens"],
        "mountain": ["Mountains", "Peaks", "Crags"],
        "ridge":["Ridge"],
        "wetland": ["Swamp","Bog", "Fen", "Marsh"],
        "gentle forest": ["Forest", "Woods", "Woodlands", "Backwoods"],
        "dark forest": ["Darkwoods","Tangle", "Rainforest", "Wilds", "Jungle"],
        "scrub":["Wastes", "Scrubland","Flats","Expanse","Rot"],
        "tundra": ["Boreal","Frost","Arctic"],
        "river": ["Creek","River","Stream", "Rapids"],
        "savanah":["Savanah"],
        "kingdom":["Kingdom"],
        "county":["Barony","County", "Nation"]
    }

    return switcher.get(what, ["Land"])


def determine_name_style(syns, name):
    """
    determine_name_style
    Parameter(s): syns - list of generated synonyms of the region type
    Return: A string to be used as a moniker for a region. Can either be in the format "The [region] of [name]" or
             or "The [Name] [Region]"
    Description: This randomly decides between two methods of arranging the region and the name.
    """
    if random.randint(1,3)==1:
        f=open(os.path.join(resources_dir, "text_files", "adjectives"),'rt')
        adjective = random.choice(f.readlines())[:-1]
        f.close()
        f=open(os.path.join(resources_dir, "text_files", "nouns"),'rt')
        noun = random.choice(f.readlines())[:-1]
        f.close()

        adjective = adjective[0].upper() + adjective[1:].lower()
        noun = noun[0].upper() + noun[1:].lower()
        if random.randint(1,2)==1:
            final_name = "The {} {} of {}s".format(adjective, random.choice(syns), noun)
        else:
            final_name = "The {} {}".format(adjective, random.choice(syns))
        return final_name
    else:
        if random.randint(1,2)==1:
            final_name = "The "
        else:
            final_name = ""
        result = random.randint(0, 100)
        if(result > 30):
            final_name += (name + " " + random.choice(syns))
        else:
            final_name += (random.choice(syns) + " of " + name)
        return final_name


def open_tables(filename):
    """
    open_table
    Parameter(s): filename - the type of style table to retrieve.
    Return: N/A
    Description: This takes in both the start_table and the mid_table and pickles them as binary files.
    """
    try:
        start_file = open(os.path.join(resources_dir, 'binary_tables',filename + '_start'), 'rb')
        start_list = pickle.load(start_file)
        start_file.close()

        mid_file = open(os.path.join(resources_dir, 'binary_tables', filename + '_mid'), 'rb')
        mid_table = pickle.load(mid_file)
        mid_file.close()
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        print("Could not find existing table that matched, creating new table from text file.")
        raise

    return mid_table, start_list


def save_tables(start_table, mid_table, filename):
    """
    save_table
    Parameter(s): start_table - the table of start characters to be saved
                  mid_table - the table of mid word syllables
                  filename - the name of the file associated with the start and mid tables
    Return: N/A
    Description: This takes in both the start_table and the mid_table and pickles them as binary files.
    """
    if not os.path.exists( os.path.join( resources_dir , 'binary_tables' )):
        os.mkdir( os.path.join( resources_dir, 'binary_tables'))

    try:
        start_file = open(os.path.join(resources_dir, 'binary_tables', filename + '_start'), 'wb')
        pickle.dump(start_table, start_file, -1)
        start_file.close()

        mid_file = open(os.path.join(resources_dir, 'binary_tables', filename + '_mid'), 'wb')
        pickle.dump(mid_table, mid_file, -1)
        mid_file.close()
    except IOError as e:
        print("The following error occurred while trying to create new table...")
        print("I/O error({0}): {1}".format(e.errno, e.strerror))
        raise

    return


def break_name_loop(name):
    """
    break_name_loop
    Parameter(s): name - the name being generated thus far
    Return: True/False
    Description: This takes in the currently generated name and decides whether or not to continue building
                     the name or cutting it short. It will ensure that all names are at least 3 characters long.
    """
    if len(name) >= 3:
        chance = 100 - len(name)*5
        if random.randint(1, 100) >= chance:
            return True
    return False
