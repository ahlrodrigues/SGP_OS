#!/bin/bash

echo "🔧 Instalando dependências para SGP_OS..."

# 1. Atualiza pacotes
sudo apt update

# 2. Instala Python 3 e pip
sudo apt install -y python3 python3-pip

# 3. Instala dependências de ambiente gráfico para o tkinter e Firefox headless
sudo apt install -y python3-tk firefox geckodriver

# 4. Cria ambiente virtual (opcional, mas recomendado)
python3 -m venv venv_envio_sgp
source venv_envio_sgp/bin/activate

# 5. Instala módulos Python necessários
pip install selenium python-dotenv

echo "✅ Ambiente configurado com sucesso!"

# 6. Instrução final
echo ""
echo "➡️ Agora você pode rodar o script com:"
echo ""
