FROM python:3.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org
CMD ["python","-u", "app.py"]