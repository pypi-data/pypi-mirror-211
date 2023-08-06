import setuptools

# COMMAND ----------

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read() 
    
setuptools.setup(
    name="data-harmonization-ai-dp",
    version="1.1.1",
    author="Himanshu",
    author_email="himanshu.tomar@decisionpoint.in",
    description="Create data quality rules and apply them to datasets.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['utility'],
    packages=['api.mapper','api.mapper.algos'],
     
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
    install_requires=['openai','pandas','fuzzywuzzy','stringmetric','rapidfuzz'],
    python_requires='>=3.8',
)