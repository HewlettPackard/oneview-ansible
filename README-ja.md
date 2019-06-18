[![Build Status](https://travis-ci.org/HewlettPackard/oneview-ansible.svg?branch=master)](https://travis-ci.org/HewlettPackard/oneview-ansible)
[![Coverage Status](https://coveralls.io/repos/github/HewlettPackard/oneview-ansible/badge.svg?branch=master)](https://coveralls.io/github/HewlettPackard/oneview-ansible?branch=master)

# Ansible Modules for HPE OneView
Ansible PlaybookでHPE OneViewを管理するAnsible用Moduleです。

## 要件

 - Ansible >= 2.1
 - Python >= 2.7.9
 - HPE OneView Python SDK ([HPE OneView Python SDKのインストールはこちら](https://github.com/HewlettPackard/python-hpOneView#installation))

## モジュールについて
本Ansible Moduleを通して、様々なOneviewの操作を行うことが可能です。また、OneViewの情報収集のためのAnsible Moduleも用意しています。

HPE OneView Ansible Module詳細に関してはこちらをご覧ください。  
  - [HPE OneView Ansible Modules Documentation](oneview-ansible.md)

### Ansible OneView modulesを使ったPlaybookの一例

```yml
- hosts: all
  tasks:

    - name: Ensure that the Fibre Channel Network is present with fabricType 'DirectAttach'
      oneview_fc_network:
        config: "/path/to/config.json"
        state: present
        data:
          name: 'New FC Network'
          fabricType: 'DirectAttach'

    - name: Ensure that Fibre Channel Network is absent
      oneview_fc_network:
        config: "/path/to/config.json"
        state: absent
        data:
          name: 'New FC Network'

    - name: Gather facts about the FCoE Network with name 'Test FCoE Network Facts'
      oneview_fcoe_network_facts:
        config: "/path/to/config.json"
        name: "Test FCoE Network Facts"
```

### サンプル

サンプルPlaybookや本Moduleを使用するための各種説明は[`ココ`](/examples)にあります。

#### その他サンプル

- HPE OneViewを使ったベアメタルサーバーの展開、HPE ICSPを使ったOSの展開、Ansibleモジュールを使ったソフトウェアのセットアップ等のDevOpsで使えるサンプルはこちらにあります。  
  - [Accelerating DevOps with HPE OneView and Ansible sample](/examples/oneview-web-farm)

- HPE Synergy Image StreamerとHPE OneViewを使ったOS展開のサンプルはこちらにあります。  
  - [HPE Synergy OS Deployment Sample](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_create_server_profile_with_deployment_plan.yml)  
  - [HPE Image Streamer Samples](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/ImageStreamer)

- HPE Synergy Image Streamerへのアーティファクトバンドルのアップロード、アーティファクトバンドルで提供されているOSビルドプランを使用してHPE OneViewにブレードサーバーをデプロイするサンプルはこちらにあります。  
  - [HPE Synergy + OneView Sample](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_image_streamer.yml).

- HPE OneViewとAnsibleを使ってベアメタルサーバーをセットアップするサンプルはこちらにあります。  
  - [C7000 Environment Setup](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/c7000_environment_setup.yml)
  - [HPE Synergy Environment Setup](https://github.com/HewlettPackard/oneview-ansible/blob/master/examples/synergy_environment_setup.yml)

## セットアップ手順
本Ansible Moduleはコンテナ化されたバージョンとフルインストールバージョンの2つが用意されています。コンテナ化されたModuleは[Docker Store](https://store.docker.com/community/images/hewlettpackardenterprise/oneview-ansible-debian)から取得できます。また、コンテナ化されたModuleのマニュアルは[こちら](https://github.com/HewlettPackard/oneview-ansible-samples/blob/master/oneview-ansible-in-container/oneview-ansible-in-container.md)から参照可能です。  

フルインストールの手順は以下となります。

### 1. Githubレポジトリのクローン

以下のコマンドを任意のディレクトリで実行します。

```bash
$ git clone https://github.com/HewlettPackard/oneview-ansible.git
```

### 2. 環境変数の設定

先ほどクローンした`oneview-ansible`内の`library`と`library/module_utils`を以下のように`ANSIBLE_LIBRARY`と`ANSIBLE_MODULE_UTILS`として環境変数に設定します。

```bash
$ export ANSIBLE_LIBRARY=/path/to/oneview-ansible/library
$ export ANSIBLE_MODULE_UTILS=/path/to/oneview-ansible/library/module_utils/
```

### 3. OneViewクライアントの設定
3種類のOneViewクライアント設定方法が選べます。
- JSON形式
- 環境変数形式
- パラメータ形式

#### JSON形式での設定
本Ansible OneView moduleはHPE OneViewに接続するための情報（パスワードやユーザー名、IP）をJSON形式で設定可能です。
設定例を以下に示します。

```json
{
  "ip": "172.25.105.12",
  "credentials": {
    "userName": "Administrator",
    "authLoginDomain": "",
    "password": "secret123"
  },
  "api_version": 200
}
```

`api_version`はHPE OneViewのREST APIバージョンの指定に使用されます。もし設定されていない場合は、`300`が指定されます。  

Proxy環境下で本moduleを実行する場合は、以下のようにProxyサーバーを本JSON設定ファイル内で指定します。
```json
  "proxy": "<proxy_host>:<proxy_port>"
```

:lock: 注意: パスワードはテキストで保存されるため、本JSON設定ファイルのパーミッションに注意してください。

本JSON設定ファイルのパスはPlaybook内の`config`に指定する必要があります。Playbook内での設定例を以下に示します。

```yml
- name: Gather facts about the FCoE Network with name 'FCoE Network Test'
  oneview_fcoe_network_facts:
    config: "/path/to/config.json"
    name: "FCoE Network Test"
```

#### 環境変数形式での設定

環境変数形式でも設定可能です。
設定例を以下に示します。

```bash
# Required
export ONEVIEWSDK_IP='172.25.105.12'
export ONEVIEWSDK_USERNAME='Administrator'
export ONEVIEWSDK_PASSWORD='secret123'

# Optional
export ONEVIEWSDK_API_VERSION='200'  # default value is 300
export ONEVIEWSDK_AUTH_LOGIN_DOMAIN='authdomain'
export ONEVIEWSDK_PROXY='<proxy_host>:<proxy_port>'
```

:lock: 注意: パスワードはテキストで保存されるため、特定のユーザーのみ環境変数を参照できる設定にしてください。  

環境変数形式で設定する場合、JSON形式での設定のようにPlaybook内に`config`を指定する必要はありません。例を以下に示します。

```yml
- name: Gather facts about the FCoE Network with name 'FCoE Network Test'
  oneview_fcoe_network_facts:
    name: "FCoE Network Test"
```

環境変数を定義した後、本Moduleを利用したPlaybookを実行できます。

#### パラメータ形式での設定

HPE OneViewの認証情報をPlaybook内のタスクに指定して設定することも可能です。

`hostname`、`username`、`password`、`api_version`、`image_streamer_hostname`、`api_version`を以下の例のように直接タスクに記載します。

```yaml
- name: Create a Fibre Channel Network
  oneview_fc_network:
    hostname: 172.16.101.48
    username: administrator
    password: my_password
    api_version: 800
    state: present
    data:
      name: "{{ network_name }}"
      fabricType: 'FabricAttach'
      linkStabilityTime: '30'
      autoLoginRedistribution: true
  no_log: true
  delegate_to: localhost
```

この設定方法の場合、PlaybookのログにHPE OneViewへの認証情報が記載されないように`no_log: true`オプションを指定することを推奨します。

### 4. HPE OneViewバージョン指定

HPE OneView Ansible moduleはHPE OneView API エンドポイントバージョン 2.0、3.0、3.10、4.0、4.10をサポートします。

デフォルトのAPIバージョンは`3.00`（300）です。

APIバージョンを指定したい場合は、前ステップで選択した設定方法を通じて、APIバージョンと認証情報を指定します。以下に例を示します。

JSON形式
```json
"api_version": 800
```

環境変数形式
```bash
export ONEVIEWSDK_API_VERSION='800'
```

APIバージョンを指定しない場合は```300```がデフォルト値として指定されます。

APIバージョンとHPE OneViewバージョンのリストは以下です。

- HPE OneView 2.0 API version: `200`
- HPE OneView 3.0 API version: `300`
- HPE OneView 3.10 API version: `500`
- HPE OneView 4.0 API version: `600`
- HPE OneView 4.10 API version: `800`

### 5. HPE Synergy Image Streamerについて

本ModuleはHPE Synergy Image Streamerに関する機能も含まれています。
HPE Synergy Image Streamerに対するModuleを使用する場合は、前述のHPE OneViewクライアント設定時にHPE Image StreamerのIPも設定する必要があります。
以下に例を示します。

JSON形式
```json
"image_streamer_ip": "100.100.100.100"
```

環境変数形式
```bash
export ONEVIEWSDK_IMAGE_STREAMER_IP='100.100.100.100'
```

サンプルのPlaybookは[こちら](https://github.com/HewlettPackard/oneview-ansible/tree/master/examples)にあります。
```image_streamer_```というPlaybook名がHPE Image Streamerに対するサンプルとなります。


## ライセンス

このプロジェクトはApache 2.0 licenseとなります。
詳細は[こちら](LICENSE)を確認してください。

## コントリビュートと機能拡張リクエストについて

**コントリビュートについて:** 本プロジェクトはコントリビュートを歓迎します。コントリビュートに関する詳細は[こちら](CONTRIBUTING.md)を確認してください。

**機能拡張リクエスト:** 
もし、現在実装されていない機能を機能拡張とリクエストする場合はNew issueからリクエストをあげてください。それらフィードバックは本プロジェクトをより良いものにするために不可欠となります。

## 命名規則について

新しいリソース/機能を追加するためには自己完結型モジュール、テスト、及びPlaybookサンプルの3つのファイルが必要です。以下は、oneview-ansibleモジュールのコード構造と命名規則の概要です。

**Module**

Moduleは**library**フォルダーに配置して下さい。すべてのモジュールは自己完結型である必要があり、hpOneView Pythonライブラリ以外の外部依存関係を作らないようにして下さい。

Moduleは**HPE OneView API Reference**のリソース名に従い、且つ単数形で命名して下さい。
ファイル名の先頭に "oneview_"を付け、全て小文字、且つスペースはアンダースコアで置き換えて下さい。  
例:** oneview_fc_network **

**テスト**

テストファイルは**tests**フォルダーに配置して下さい。ファイル名は"test_"から始まるように命名して下さい。  
例: **test_oneview_fc_network**

**Playbookサンプル**

サンプルPlaybookは**examples**フォルダーにModule名と同じ名前で配置して下さい。  
例: **oneview_fc_network.yml**

**Facts**

Facts Moduleも他のModule同様のルールに従います。ファイル名は"\_facts"のように命名して下さい。  
例: **oneview_fc_network_facts**

## テストについて
基本的なテストは`build.sh`ファイルの実行で行われます。テストに関する詳細は[こちら](TESTING.md)を確認して下さい。
