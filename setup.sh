sudo apt install python3.12-venv

python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/ansible-galaxy install -r requirements.yml

git clone https://github.com/kubernetes-sigs/kubespray.git
.venv/bin/pip install -r kubespray/requirements.txt
#wget https://raw.githubusercontent.com/kubeovn/kube-ovn/release-1.12/dist/images/kubectl-ko