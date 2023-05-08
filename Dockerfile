FROM nvidia/cuda:11.0-cudnn8-devel-ubuntu18.04 AS builder

RUN sed -i 's#archive.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list  \
    && sed -i 's#security.ubuntu.com#mirrors.aliyun.com#g' /etc/apt/sources.list

ENV LANG=zh_CN.UTF-8 LANGUAGE=zh_CN:zh LC_ALL=zh_CN.UTF-8 DEBIAN_FRONTEND=noninteractive

RUN rm -rf  /etc/apt/sources.list.d/  && apt update

RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor \
    iputils-ping \
    wget \
    zsh \
    build-essential \
    cmake \
    git \
    curl \
    vim \
    ca-certificates \
    openssh-server \
    language-pack-zh-hans \
    ttf-wqy-zenhei \
    libgl1-mesa-glx  \
    libglib2.0-0 \
    locales \
    libmagic1

RUN locale-gen zh_CN.UTF-8
RUN dpkg-reconfigure locales

CMD ["supervisord", "-n"]


# 配置ssh
FROM builder as builder1
RUN mkdir /var/run/sshd
RUN echo 'root:113113' | chpasswd
RUN sed -i 's/.*PermitRootLogin .*/PermitRootLogin yes/' /etc/ssh/sshd_config
# SSH login fix. Otherwise user is kicked off after login
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd
RUN echo "\
[program:sshd] \n\
command=/usr/sbin/sshd -D\n\
autorestart=True\n\
autostart=True\n\
redirect_stderr = true\n\
" > /etc/supervisor/conf.d/sshd.conf
EXPOSE 22

# 配置zsh
FROM builder1 as builder2
RUN wget https://gitee.com/mirrors/oh-my-zsh/raw/master/tools/install.sh -O /root/install.sh
RUN sed -i 's#REPO=${REPO:-ohmyzsh/ohmyzsh}#REPO=${REPO:-mirrors/oh-my-zsh}#g' /root/install.sh && \
    sed -i 's#REMOTE=${REMOTE:-https://github.com/${REPO}.git}#REMOTE=${REMOTE:-https://gitee.com/${REPO}.git}#g' /root/install.sh && \
    chmod +777 /root/install.sh && \
    ./root/install.sh && \
    rm /root/install.sh
RUN git clone https://kgithub.com/Zeke-chin/my-config /root/my-config && \
    rm /root/.zshrc && \
    ln -s /root/my-config/.zshrc /root/.zshrc
RUN git clone https://kgithub.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions && \
    git clone https://kgithub.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
RUN chsh -s `which zsh`

# 配置conda、mamba
FROM builder2 as builder3
ENV PYTHON_VERSION 3
RUN chsh -s `which zsh`
RUN curl -o ~/miniconda.sh -O  https://repo.anaconda.com/miniconda/Miniconda${PYTHON_VERSION}-latest-Linux-x86_64.sh  && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh
RUN ln /opt/conda/bin/conda /usr/local/bin/conda
RUN conda init zsh
RUN conda install mamba -n base -c conda-forge
RUN ln /opt/conda/bin/mamba /usr/local/bin/mamba && mamba init zsh

# 配置server
FROM builder3 as builder4
ENV WORKDIR /workspace
WORKDIR ${WORKDIR}
ADD environment.yml /environment.yml
RUN mamba update -n base -c defaults conda -y && mamba env create -f /environment.yml && rm -rf /root/.cache

RUN echo "\
[program:be]\n\
directory=/workspace\n\
command=/opt/conda/envs/py10/bin/gunicorn server:app --workers 1 --worker-class uvicorn.workers.UvicornWorker  --bind 0.0.0.0:8080 --reload\n\
autorestart=true\n\
startretries=100\n\
redirect_stderr=true\n\
stdout_logfile=/var/log/be.log\n\
stdout_logfile_maxbytes=50MB\n\
environment=PYTHONUNBUFFERED=1, PYTHONIOENCODING=utf-8\n\
" > /etc/supervisor/conf.d/be.conf


