FROM python:3.6-slim-buster

LABEL maintainer "Chebrolu Harika <bala-sai-harika.chebrolu@hpe.com>"

WORKDIR /root

# Some optional but recommended packages
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get update -y \
    && apt-get install --no-install-recommends -y \
    vim \
    curl \
    ansible

RUN pip install pyOpenSSL hpOneView

ADD . oneview-ansible/

WORKDIR /root/oneview-ansible

# Adding hosts for convenience
RUN mkdir -p /etc/ansible
RUN echo [localhost] >> /etc/ansible/hosts
RUN echo localhost ansible_python_interpreter=python3 ansible_connection=local >> /etc/ansible/hosts

# packages to run tests
RUN cd /root/oneview-ansible/
RUN pip install -r test_requirements.txt

ENV ANSIBLE_LIBRARY=/root/oneview-ansible/library
ENV ANSIBLE_MODULE_UTILS=/root/oneview-ansible/library/module_utils/

# Clean and remove not required packages
RUN DEBIAN_FRONTEND=noninteractive \
    apt-get autoremove -y && \
    apt-get clean -y && \
    rm -rf /var/cache/apt/archives/* /var/cache/apt/lists/* /tmp/* /root/cache/.

CMD [ "ansible-playbook", "--version" ]
