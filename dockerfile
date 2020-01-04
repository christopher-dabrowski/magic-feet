FROM python:3

EXPOSE 8050

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY feet_animation/dist/feet_animation-0.0.1.tar.gz feet_animation-0.0.1.tar.gz
RUN pip install --no-cache-dir feet_animation-0.0.1.tar.gz

COPY assets assets
COPY index.py .

CMD [ "python", "index.py" ]