import re
import pprint
JOB_DESCRIPTIONS_TEXT_FILE_PATH = 'job descriptions.txt'
pp = pprint.PrettyPrinter(indent=4)

# Mapping of x to y that is used to replace every instance of x with y in the tex string
latex_escaped_chars_replacement_map = (
    ('\\\\&', '&'),
    ('\\\\\$', '$'),
    ('\\\\textit\\{NCR\\}', 'NCR'),
    ('\\\\texttt\\{\+\\}', '+'),
    ('\\\\nth\\{1\\}', '1st'),
    # ('\\\\%', '%'),
)

# Object to hold one Work Experience listing
class Work_Exp_Listing():

    def __init__(self, date_range="", title="", company="", city="", state="", description_list=[]):
        self.date_range = date_range
        self.title = title
        self.company = company
        self.city = city
        self.state = state
        self.location = f'{city}, {state}'
        self.description_list = description_list
    
    def __repr__(self):
        description_list = '- ' + '\n- '.join(self.description_list)
        return f'Job Title\n{self.title}\n\nCompany\n{self.company}\n\nLocation\n{self.location}\n\n{description_list}'

# Object to represent the entire Work Experience section
class Work_Exp():

    def __init__(self, work_exp_listings=[]):
        self.work_exp_listings = work_exp_listings
    
    def __repr__(self):
        return '\n\n\n\n'.join([str(x) for x in self.work_exp_listings])

# Open the tex file as a string
with open('cv.tex', 'r') as f:
    texfile = f.read()

# Extract the Work Experience section as a string
work_experience_contents = re.search('\\\\section{Work Experience}\n((.|\n)*)\\\\section{Projects}', texfile).group(1)

# Unindent each line by one tab
work_experience_contents = re.sub('\n\t', '\n', work_experience_contents)
work_experience_contents = re.sub('^\t', '', work_experience_contents)

# Use the mapping to replace every escaped tex char/macro with the plaintext version
for find_str, sub_str in latex_escaped_chars_replacement_map:
    work_experience_contents = re.sub(find_str, sub_str, work_experience_contents)
# work_experience_contents = re.sub('^\\t[^\\t]*$', '', work_experience_contents)

# Separate each job into its own string
each_work_experience_listing = work_experience_contents.split('\\cventry')[1:]

def get_one_work_experience_listing(one_work_listing):
    # Unindent each line by one tab
    one_work_listing = re.sub('\\t', '', one_work_listing)
    # Get rid of the \item enumeration from each bullet point
    one_work_listing = re.sub('\\\item ', '', one_work_listing)
    # Separate (metadata and) each bullet point into its own string
    one_work_listing = one_work_listing.strip().split('\n')
    # Define the metadata of a job, like date_range, title, etc.
    metadata = one_work_listing[0]
    # Further split the metadata that's wrapped in curly brackets
    metadata_split = re.findall('{([^{}]*)}', metadata)
    # Extract only the bullet points from the list
    description_list = one_work_listing[2:-2]

    return Work_Exp_Listing(*metadata_split, description_list)

# Create the entire Work Experience section
work_exp = Work_Exp([get_one_work_experience_listing(x) for x in each_work_experience_listing])

with open('job descriptions.txt', 'w') as f:
    f.write(str(work_exp))