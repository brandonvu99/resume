import ruamel.yaml
yaml = ruamel.yaml.YAML()
yaml.indent(sequence=4)
import re
import pprint
pp = pprint.PrettyPrinter(indent=4)
import os

EDUCATION_YAML_FILE_PATH = 'sections_extracted/education.yaml'
EDUCATION_TEXT_FILE_PATH = 'sections_extracted/education.txt'
JOB_DESCRIPTIONS_YAML_FILE_PATH = 'sections_extracted/job_descriptions.yaml'
JOB_DESCRIPTIONS_TEXT_FILE_PATH = 'sections_extracted/job_descriptions.txt'
PROJECTS_YAML_FILE_PATH = 'sections_extracted/projects.yaml'
PROJECTS_TEXT_FILE_PATH = 'sections_extracted/projects.txt'
SKILLS_YAML_FILE_PATH = 'sections_extracted/skills.yaml'
SKILLS_TEXT_FILE_PATH = 'sections_extracted/skills.txt'
ALL_FILE_PATHS_TO_EXTRACTED_DATA = [
    EDUCATION_YAML_FILE_PATH,
    EDUCATION_TEXT_FILE_PATH,
    JOB_DESCRIPTIONS_YAML_FILE_PATH,
    JOB_DESCRIPTIONS_TEXT_FILE_PATH,
    PROJECTS_YAML_FILE_PATH,
    PROJECTS_TEXT_FILE_PATH,
    SKILLS_YAML_FILE_PATH,
    SKILLS_TEXT_FILE_PATH,
]
for file_path in ALL_FILE_PATHS_TO_EXTRACTED_DATA:
    if os.path.exists(file_path):
        os.remove(file_path)

# Mapping of x to y that is used to replace every instance of x with y in the tex string
latex_escaped_chars_replacement_map = (
    (r'\\&', '&'),
    (r'\\$', '$'),
    (r'\\texttt\{\+\}', '+'),
    (r'\\nth\{1\}', '1st'),
    (r'\\%', '%')
)

def extract_education():
    # Object to hold one Education listing
    class Education_Listing():
        def __init__(self, date_start="", date_end="", degree_title="", school_name="", city="", state="", description_list=[]):
            self.date_start = date_start
            self.date_end = date_end
            self.degree_title = degree_title
            self.school_name = school_name
            self.city = city
            self.state = state
            self.description_list = description_list
    yaml.register_class(Education_Listing)

    # Open the tex file as a string
    with open('cv.tex', 'r') as f:
        texfile = f.read()

    # Extract the Education section as a string
    education_contents = re.search('\\\\section{Education}\n((.|\n)*)\\\\section{Work Experience}', texfile).group(1)

    # Unindent each line by one tab
    education_contents = re.sub('\n\t', '\n', education_contents)
    education_contents = re.sub('^\t', '', education_contents)

    # Remove tex comments
    education_contents = re.sub(r'%.*\n', '\n', education_contents)

    # Remove \begin{itemize}\end{itemize} section
    education_contents = re.sub(r'\\begin{itemize}', '', education_contents)
    education_contents = re.sub(r'\\end{itemize}', '', education_contents)

    # Use the mapping to replace every escaped tex char/macro with the plaintext version
    for find_str, sub_str in latex_escaped_chars_replacement_map:
        education_contents = re.sub(find_str, sub_str, education_contents)

    # Separate each education into its own string
    each_education_contents = education_contents.split(r'\cventry')[1:]

    def get_one_education_listing(one_education_listing):
        # Unindent each line by one tab
        one_education_listing = re.sub('\\t', '', one_education_listing)
        # Get rid of the \item enumeration from each bullet point
        one_education_listing = re.sub('\\\item ', '', one_education_listing)
        # Separate (metadata and) each bullet point into its own string
        one_education_listing = one_education_listing.strip().split('\n')
        # Define the metadata of a job, like date_range, title, etc.
        metadata = one_education_listing[0]
        # Further split the metadata that's wrapped in curly brackets
        date_range, title, company, city, state = re.findall('{([^{}]*)}', metadata)
        # Split the date_range into date_start and date_end
        date_start, date_end = date_range.split(' -- ')
        # Extract only the bullet points from the list
        description_list = one_education_listing[2:-1]

        return Education_Listing(date_start, date_end, title, company, city, state, description_list)

    # Create the entire Education section
    education = [get_one_education_listing(x) for x in each_education_contents]

    with open(EDUCATION_YAML_FILE_PATH, 'w') as f:
        yaml.dump(education, f)

def extract_job_descriptions_to_txt():
    # Mapping of x to y that is used to replace every instance of x with y in the tex string
    latex_escaped_chars_replacement_map_override = (
        (r'\\&', '&'),
        (r'\\$', '$'),
        (r'\\textit\{NCR\}', 'NCR'),
        (r'\\textit\{Capital One\}', 'Capital One'),
        (r'\\texttt\{\+\}', '+'),
        (r'\\nth\{1\}', '1st'),
        (r'\\%', '%'),
        (r'\\textbf\{live\}', 'live')
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
            return f'Company\n{self.company}\n\n' + \
                f'Job Title\n{self.title}\n\n' + \
                f'Dates\n{self.date_range}\n\n' + \
                f'Location\n{self.location}\n\n' + \
                f'{description_list}'

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

    # Remove \begin{itemize}\end{itemize} section
    work_experience_contents = re.sub(r'\\begin{itemize}', '', work_experience_contents)
    work_experience_contents = re.sub(r'\\end{itemize}', '', work_experience_contents)

    # Use the mapping to replace every escaped tex char/macro with the plaintext version
    for find_str, sub_str in latex_escaped_chars_replacement_map_override:
        work_experience_contents = re.sub(find_str, sub_str, work_experience_contents)
    # work_experience_contents = re.sub('^\\t[^\\t]*$', '', work_experience_contents)

    # latex_special_escaped_chars = ('&', '$', '%')
    # regex_pattern = r'\\(?!cventry)[a-zA-z]*{(.*)}' + \
    #                 r'|' + \
    #                 r'\\([' + ''.join(latex_special_escaped_chars) + "])"
    # work_experience_contents = re.sub(regex_pattern, r'\1\2', work_experience_contents)

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

    # Gets back a list of tuples (line number, char number in line, actual line) of regex matches within src
    def get_matching_line_num_and_line(regex, src):
        # Separate each line into its own string
        lines = src.split('\n')
        matches = []
        # Iterate over those lines
        for line_num, line in enumerate(lines):
            # Check if the regex exist in this line
            match = re.search(regex, line)
            # If it does, make and add the tuple as specified in the function docs
            if match is not None:
                matches.append((line_num, match.span()[0], line))
        return matches

    # Check if there are any unhandled escaped chars/macros. If there are, throw an error and don't save the file
    work_exp_as_text = str(work_exp)
    unhandled_escape_chars = get_matching_line_num_and_line('\\\\', work_exp_as_text)

    # Pretty print unhandled escape chars
    def string_pretty_print_unhandled_escape_chars(unhandled_escape_chars):
        pretty_strings = []
        for line_num, char_num, line in unhandled_escape_chars:
            pretty_strings.append(f'{line_num}:{char_num}\t{line}')
        return '\n'.join(pretty_strings)

    if len(unhandled_escape_chars) > 0:
        print('Found an unescaped character at the following line_num:char_num_in_line pairs:\n' + string_pretty_print_unhandled_escape_chars(unhandled_escape_chars))
    else:
        with open(JOB_DESCRIPTIONS_TEXT_FILE_PATH, 'w') as f:
            f.write(work_exp_as_text)

def extract_job_descriptions():
    # Object to hold one Work Experience listing
    class Work_Exp_Listing():
        def __init__(self, date_start="", date_end="", title="", company="", city="", state="", description_list=[]):
            self.date_start = date_start
            self.date_end = date_end
            self.title = title
            self.company = company
            self.city = city
            self.state = state
            self.description_list = description_list
    yaml.register_class(Work_Exp_Listing)
    
    # Open the tex file as a string
    with open('cv.tex', 'r') as f:
        texfile = f.read()

    # Extract the Work Experience section as a string
    work_experience_contents = re.search('\\\\section{Work Experience}\n((.|\n)*)\\\\section{Projects}', texfile).group(1)

    # Unindent each line by one tab
    work_experience_contents = re.sub('\n\t', '\n', work_experience_contents)
    work_experience_contents = re.sub('^\t', '', work_experience_contents)

    # Remove \begin{itemize}\end{itemize} section
    work_experience_contents = re.sub(r'\\begin{itemize}', '', work_experience_contents)
    work_experience_contents = re.sub(r'\\end{itemize}', '', work_experience_contents)

    # Use the mapping to replace every escaped tex char/macro with the plaintext version
    for find_str, sub_str in latex_escaped_chars_replacement_map:
        work_experience_contents = re.sub(find_str, sub_str, work_experience_contents)

    # Separate each job into its own string
    each_work_experience_listing = work_experience_contents.split(r'\cventry')[1:]

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
        date_range, title, company, city, state = re.findall('{([^{}]*)}', metadata)
        # Split the date_range into date_start and date_end
        date_start, date_end = date_range.split(' -- ')
        # Extract only the bullet points from the list
        description_list = one_work_listing[2:-2]

        return Work_Exp_Listing(date_start, date_end, title, company, city, state, description_list)

    # Create the entire Work Experience section
    work_exp = [get_one_work_experience_listing(x) for x in each_work_experience_listing]

    with open(JOB_DESCRIPTIONS_YAML_FILE_PATH, 'w') as f:
        yaml.dump(work_exp, f)

def extract_projects():
    # Object to hold one Project listing
    class Project_Listing():
        def __init__(self, name="", description=""):
            self.name = name
            self.description = description
    yaml.register_class(Project_Listing)

    # Open the tex file as a string
    with open('cv.tex', 'r') as f:
        texfile = f.read()

    # Extract the Project section as a string
    project_contents = re.search('\\\\section{Projects}\n((.|\n)*)\\\\section{Skills}', texfile).group(1)

    # Unindent each line by one tab
    project_contents = re.sub('\n\t', '\n', project_contents)
    project_contents = re.sub('^\t', '', project_contents)

    # Remove tex comments
    project_contents = re.sub(r'%.*\n', '\n', project_contents)

    # Remove \begin{itemize}\end{itemize} section
    project_contents = re.sub(r'\\begin{itemize}', '', project_contents)
    project_contents = re.sub(r'\\end{itemize}', '', project_contents)

    # Use the mapping to replace every escaped tex char/macro with the plaintext version
    for find_str, sub_str in latex_escaped_chars_replacement_map:
        project_contents = re.sub(find_str, sub_str, project_contents)

    # Separate each project into its own string
    each_project_contents = project_contents.split(r'\cvlistitem')[1:]

    def get_one_project_listing(one_project_listing):
        # Unindent each line by one tab
        one_project_listing = re.sub('\\t', '', one_project_listing)
        # Get the project name which looks like \textbf{Karaoke Queuer}
        name = re.search(r'\\textbf{(.*)}, ', one_project_listing).group(1)
        description = re.search(r'\\textbf{.*}, (.*)}', one_project_listing).group(1)
        return Project_Listing(name, description)

    # Create the entire Work Experience section
    projects = [get_one_project_listing(x) for x in each_project_contents]

    with open(PROJECTS_YAML_FILE_PATH, 'w') as f:
        yaml.dump(projects, f)

def extract_skills():
    
    # Object to hold one Skill listing
    class Skill_Listing():
        def __init__(self, skill_category="", skill_list=""):
            self.skill_category = skill_category
            self.skill_list = skill_list
    yaml.register_class(Skill_Listing)

    # Open the tex file as a string
    with open('cv.tex', 'r') as f:
        texfile = f.read()

    # Extract the Skills section as a string
    skills_contents = re.search('\\\\section{Skills}\n((.|\n)*)\\\\section{Interests}', texfile).group(1)

    # Unindent each line by one tab
    skills_contents = re.sub('\n\t', '\n', skills_contents)
    skills_contents = re.sub('^\t', '', skills_contents)

    # Remove tex comments
    skills_contents = re.sub(r'%.*\n', '\n', skills_contents)

    # Remove \begin{itemize}\end{itemize} section
    skills_contents = re.sub(r'\\begin{itemize}', '', skills_contents)
    skills_contents = re.sub(r'\\end{itemize}', '', skills_contents)

    # Use the mapping to replace every escaped tex char/macro with the plaintext version
    for find_str, sub_str in latex_escaped_chars_replacement_map:
        skills_contents = re.sub(find_str, sub_str, skills_contents)

    # Separate each skill into its own tuple (skill_category, skill_list). The ? modifier on * makes the * non-greedy
    skills_contents = re.findall(r'{(.*?)}', skills_contents)
    skills = []
    for i in range(0, len(skills_contents), 2):
        category = skills_contents[i].replace(":", "")
        skill_list_as_one_string = skills_contents[i+1]
        if not category and not skill_list_as_one_string:
            continue
        skill_list = skill_list_as_one_string.split(', ')
        skills.append(Skill_Listing(category, skill_list))

    with open(SKILLS_YAML_FILE_PATH, 'w') as f:
        yaml.dump(skills, f)

extract_education()
extract_job_descriptions()
extract_projects()
extract_skills()