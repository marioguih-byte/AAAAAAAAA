# Precipitação horária · Unidades Petrobras

App Streamlit que lê a previsão do **Google WeatherNext 3** (via [dynamical.org](https://dynamical.org),
pacote `dynamical-catalog`) e mostra a precipitação nos pontos das 40 unidades:

- mapa interativo com as unidades coloridas pelo valor;
- **acumulado em um intervalo** escolhido por você (slider de início/fim, com atalhos de 6, 12, 24 e 48 h, Hoje, Amanhã e Tudo);
- **hora a hora**, com slider e animação;
- escolha de inicialização, estatística (padrão `mean`) e amostragem (bilinear ou vizinho mais próximo);
- série temporal da unidade (ou média das 40), ranking e download em CSV.

## Rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Requer Python 3.11 ou mais novo (o `zarr` 3 exige) e acesso à internet.

## Publicar no Streamlit Community Cloud

1. Suba esta pasta para um repositório no GitHub (`streamlit_app.py` e `requirements.txt` na raiz).
2. Em share.streamlit.io, crie o app apontando para `streamlit_app.py`.
3. Se alterar o `requirements.txt`, use *Reboot app* em *Manage app*.

## Como os valores são calculados

- A variável padrão é `precipitation_surface` (kg m⁻² s⁻¹ = mm/s), do catálogo
  `google-weathernext3-forecast-48-hour-0-1-degree-virtual`. Ambos podem ser trocados em *Catálogo (avançado)*.
- Cada valor vira mm no passo: taxa × 3600 × duração do passo. O app detecta o passo de tempo do dataset.
- O valor de cada instante é a chuva do passo que **termina** nele. O acumulado entre A e B soma os passos
  depois de A até B, inclusive (08/11 15h → 09/11 15h = 24 h).
- Horário exibido: Brasília (America/Sao_Paulo).
- Os pontos são lidos da grade de 0,1° por interpolação bilinear (ou célula mais próxima).

## Unidades

Nomes e coordenadas vêm do cadastro `ESTACOES_PADRAO` do projeto `rio-raios`. Para adicionar ou alterar
unidades, edite a lista `UNIDADES` no início do `streamlit_app.py`.
