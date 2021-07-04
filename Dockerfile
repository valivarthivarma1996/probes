
FROM python
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 9000
CMD ["python", "app.py"]
