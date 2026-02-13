FROM python:3.12-slim

#RUN pip install "django<6" gunicorn whitenoise
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

#install  ตาม requirements
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY src /src
WORKDIR /src

RUN DJANGO_SECRET_KEY=build_only python manage.py collectstatic --noinput
ENV DJANGO_DEBUG_FALSE=1

RUN adduser --uid 1234 nonroot  
USER nonroot

#CMD python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8888
CMD ["gunicorn", "--bind", ":8888", "superlists.wsgi:application"]