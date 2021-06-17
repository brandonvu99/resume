# Brandon Vu's Resume

This is a repo containing my resume. To get the most up to date resume, you will need to build the `.pdf` of the resume; otherwise, check releases for a somewhat (or most up to date if I remember to do a release) version.

# How to Build
1. Install LaTeX
2. Install Python
3. Build `cv.tex` using `pdflatex` or equivalent.
    - An `UnescapedCharCheck` error during building means that the `extract_job_desciptions.py` script found line in the job description section that uses an escaped character (like `\textit{}` or `\texttt{}`) that was not explicitly listed in the list of tuples called `latex_escaped_chars_replacement_map`. The first element of each tuple are strings found in the `cv.tex` file that will be replaced by the second element of each tuple for the `job descriptions.txt` file that will be generated.
