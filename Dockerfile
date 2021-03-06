FROM        juliahwang/weatherpractice
MAINTAINER  qufskan9396@gmail.com

ENV         LANG C.UTF-8

# 현재 경로의 모든 파일들을 컨테이너의 /srv/deploy_eb/docker 폴더에 복사
COPY        . /srv/00_practice
# cd /srv/deploy_eb/docker 와 같음
WORKDIR     /srv/00_practice

# requiremments.txt 설치
RUN         /root/.pyenv/versions/prac_teamproject/bin/pip install -r .requirements/deploy.txt

# supervisor 파일 복사
COPY        .config/supervisor/uwsgi.conf /etc/supervisor/conf.d/
COPY        .config/supervisor/nginx.conf /etc/supervisor/conf.d/

# nginx 설정파일, nginx 사이트 파일 복사
COPY        .config/nginx/nginx.conf /etc/nginx/
COPY        .config/nginx/nginx-app.conf /etc/nginx/sites-available/

# nginx 링크 작성
RUN         ln -sf /etc/nginx/sites-available/nginx-app.conf /etc/nginx/sites-enabled/nginx.conf
RUN         rm -rf /etc/nginx/sites-enabled/default

# collectstatic 실행
RUN         /root/.pyenv/versions/prac_teamproject/bin/python /srv/00_practice/django_app/manage.py collectstatic --settings=config.settings.deploy --noinput

CMD         supervisord -n
# 80포트와 8000포트를 열어줌
EXPOSE      80 8000
