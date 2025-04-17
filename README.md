<p align="center" width="100%">
    <img src="https://bytebucket.org/ahlrodrigues/slackonfig/raw/adca69d05d4b9db0ee9cfa65f54cad4e87dabad7/imgs/Slackware1.png">
</p>



**SLACKONFIG** - um scripts para configuração do Slackware GNU/Linux e instalação de algumas "firulas".
--------------



>Autor: Antonio Henrique (Fela)

>E-mail: ahlr_2000@yahoo.com

>Telegram: @Antonio_Henrique_Fela

>Matrix: @antonio_pu2ysh:matrix.org

>[Grupo Slackshowbr no Telegram](https://t.me/slackshowbr)



>Bugs, Agradecimentos, Críticas "construtivas", mande um e-mail, ficarei Grato!



**Nota:**
----------
```
Os scripts deste diretório estão disponíveis na esperança que possam ser úteis, mas SEM NENHUMA
GARANTIA DE FUNCIONAMENTO, SEM NENHUMA GARANTIA DE ADEQUAÇÃO A QUALQUER MERCADO, SEM NENHUMA
GARANTIA DE APLICAÇÃO EM PARTICULAR e NENHUM SUPORTE TÉCNICO.

Ah! alguns scripts podem sumir inesperadamente por ação de forças estranhas
independente da nossa vontade.
```


**Scripts e Funções:**
----------------------
```
Este pequeno script roda em "silêncio", abre um navegador, loga-se no [SGP](https://www.tsmx.net.br/sgp/),
gera um relatório de ordens de serviço em aberto com alguns técnicos, exporta o relatório par o formato xlsx
e baixa na pasta download do usuário.

```


Usage:
------
```
1. logue-se como root
2. Descompacte o arquivo SGP_OS.tar.gz na pasta /opt (tar -xvf SGP_OS.tar.gz -C /opt)
3. Acrescente seu login e senha do SGP no arquivo /opt/SGP/.env
4. Abra o crontab (crontab -e)
5. Acrescente a linha para rodar o script todos os dias às 16:30 (30 16 * * * /usr/bin/python3 /opt/SGP/SGP_OS.py)
6. Rode o script setup.sh para configurar o ambiente (chmod +x & /opt/setup.sh)
6. Teste o script, se funcionar manualmente, também funcionará pelo cron (python /opt/SGP_OS.py)

```


**GNU General Public License:**
-------------------------------
```
Estes scripts/programas são softwares livres, você pode redistribuí-los e/ou modifica-los
dentro dos termos da Licença Pública Geral GNU:
```
> [General Public License](https://pt.wikipedia.org/wiki/GNU_General_Public_License)
>
>Fundação do Software Livre (FSF) Inc. 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

<p align="center" width="100%">
    <img src="https://bytebucket.org/ahlrodrigues/slackonfig/raw/adca69d05d4b9db0ee9cfa65f54cad4e87dabad7/imgs/poweredbyslack.gif">
</p>
