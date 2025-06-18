============================================================
📺 UrbanTV XMLTV - Conversor e Monitorador de EPG (Windows)
============================================================

Este projeto possui dois scripts principais para obter e manter atualizados os arquivos de programação (EPG) da UrbanTV convertidos no padrão XMLTV:

  1. 🔁 Monitor automático de atualizações (urbantv_monitor)
  2. 🔄 Conversor manual de XML para XMLTV (converter_urban_drive)

Ambos funcionam em Windows, tanto com Python quanto como executáveis .exe.

------------------------------------------------------------
📂 Estrutura da pasta
------------------------------------------------------------

C:\Users\SeuNome\Desktop\urban_drive_xmltv\
├── converter_urban_drive.py         → Converte o Urban-Drive manualmente
├── urbantv_monitor.py               → Monitora e converte Otaku, Urban-Drive e Urban-Travel
├── UrbanDrive_XMLTV.xml             → XMLTV convertido do canal Urban-Drive
├── UrbanTravel_XMLTV.xml            → XMLTV convertido do canal Urban-Travel
├── Otaku_XMLTV.xml                  → XMLTV convertido do canal Otaku
├── urbantv_state.json               → Guarda estado de verificação (ETag, Last-Modified)
├── dist\                            → Pasta com os arquivos .exe gerados
│   ├── converter_urban_drive.exe
│   └── urbantv_monitor.exe
├── README.txt                       → Este guia

------------------------------------------------------------
🧰 Requisitos
------------------------------------------------------------

✔️ Python 3.8+ instalado: https://www.python.org/downloads/windows/  
✔️ Biblioteca `requests` instalada:

Abra o `CMD` e execute:

    pip install requests

✔️ (Opcional) PyInstaller para gerar os `.exe`:

    pip install pyinstaller

------------------------------------------------------------
🚀 Como executar os scripts Python (.py)
------------------------------------------------------------

1. Abra o Prompt de Comando (CMD)
2. Vá até a pasta do projeto:

    cd C:\Users\SeuNome\Desktop\urban_drive_xmltv

3. Para **converter manualmente o Urban-Drive**:

    python converter_urban_drive.py

4. Para **iniciar o monitoramento automático dos canais**:

    python urbantv_monitor.py

Isso manterá atualizados os arquivos `Otaku_XMLTV.xml`, `UrbanDrive_XMLTV.xml`, e `UrbanTravel_XMLTV.xml` a cada 15 minutos (configurável no script).

------------------------------------------------------------
🖥️ Como executar como programa .EXE (sem Python)
------------------------------------------------------------

Se você já tiver a pasta `dist/` com os arquivos `.exe`, basta:

✅ Dar **duplo clique** nos arquivos `converter_urban_drive.exe` ou `urbantv_monitor.exe`, ou

✅ Executar pelo terminal:

    dist\converter_urban_drive.exe
    dist\urbantv_monitor.exe

Eles funcionam sem precisar abrir o Python — ideal para uso em servidor, automação ou por usuários comuns.

Se **ainda não tiver** os `.exe`, crie-os com:

    pyinstaller --onefile --clean converter_urban_drive.py
    pyinstaller --onefile --clean urbantv_monitor.py

Os executáveis serão salvos automaticamente na pasta `dist\`.

------------------------------------------------------------
📌 Notas Finais
------------------------------------------------------------

✅ Scripts funcionam tanto com Python quanto como `.exe`  
✅ XMLTV compatível com Kodi, VLC, IPTV Smarters, TVheadend e outros  
✅ Perfeito para automação e distribuição de EPG personalizada  
✅ Código 100% offline e sob seu controle  

---

🧑‍💻 Autor: onepadev@gmail.com
🗓️ Última atualização: Junho 2025  
🌐 Projeto: UrbanTV XMLTV Tools
