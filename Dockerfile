FROM python:3.7

ENV PYTHONBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY . /code/

RUN pip install virtualenvwrapper
RUN pip install setuptools pip --upgrade --force-reinstall
ENV PYTHONPATH "${PYTHONPATH}:/code"

RUN virtualenv /venv
RUN /bin/bash -c "source /venv/bin/activate"

RUN pip install -r requirements.txt

CMD cherryd -i main
