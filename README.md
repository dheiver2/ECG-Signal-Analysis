
# ECG Signal Analysis Toolkit

Este repositório contém uma ferramenta para análise e visualização de sinais ECG (Eletrocardiograma). O projeto inclui funcionalidades para segmentação de sinais ECG, plotagem de gráficos e cálculo de métricas importantes, como frequência cardíaca, variabilidade da frequência cardíaca (HRV), e análise espectral. Também é possível detectar e salvar informações sobre picos R, artefatos e complexidade do sinal.

## Funcionalidades

- **Divisão e Plotagem do Sinal ECG**: O sinal ECG é dividido em segmentos, e os gráficos de cada segmento são gerados e visualizados com os picos R destacados.
- **Cálculo de Métricas**: O projeto calcula várias métricas do sinal ECG, incluindo:
  - Frequência Cardíaca (bpm)
  - Intervalos PR e QT
  - Duração do Complexo QRS
  - Variabilidade da Frequência Cardíaca (HRV)
  - Amplitude dos Picos R
  - Análise de Complexidade (Entropia e Dimensão Fractal)
  - Detecção de Artefatos e Ruídos
  - Power Spectral Density (PSD)
- **Armazenamento em JSON**: As métricas calculadas e os dados dos gráficos gerados são salvos em arquivos JSON para posterior análise.

## Pré-requisitos

Para rodar o código, você precisa ter o seguinte instalado:

- Python 3.x
- Bibliotecas Python:
  - `numpy`
  - `matplotlib`
  - `scipy`
  - `seaborn`
  - `wfdb`
  - `json`

Você pode instalar as dependências com o seguinte comando:

```bash
pip install numpy matplotlib scipy seaborn wfdb
```

## Estrutura do Projeto

```
ECG-Signal-Analysis-Toolkit/
├── ecg_plotter.py          # Código principal da análise ECG
├── ecg_graph_data.json     # Arquivo JSON com os dados dos gráficos
├── ecg_metrics.json        # Arquivo JSON com as métricas calculadas
├── README.md               # Este arquivo
```

## Uso

### 1. Carregando o Registro ECG

Primeiro, você precisa carregar um registro ECG usando a biblioteca `wfdb`. O arquivo deve ser em formato `.dat` ou um arquivo de registro compatível.

Exemplo de como carregar um arquivo ECG:

```python
import wfdb

# Substitua pelo caminho correto do arquivo
record = wfdb.rdrecord('/caminho/para/o/arquivo')
```

### 2. Instanciando a Classe `ECGPlotter`

Crie uma instância da classe `ECGPlotter` passando o registro ECG carregado como parâmetro.

```python
from ecg_plotter import ECGPlotter

# Defina o número de partes e amostras por parte
ecg_plotter = ECGPlotter(record, num_parts=12, samples_per_part=5000)
```

### 3. Plotando os Segmentos do ECG

Chame o método `plot_segments()` para gerar e exibir os gráficos dos segmentos do sinal ECG.

```python
ecg_plotter.plot_segments()
```

Este método também salvará os dados dos gráficos em um arquivo JSON chamado `ecg_graph_data.json`.

### 4. Calculando as Métricas do ECG

Chame o método `calculate_metrics()` para calcular as métricas do sinal ECG e salvá-las em um arquivo JSON.

```python
ecg_plotter.calculate_metrics()
```

Este método salva as métricas em `ecg_metrics.json`.

## Exemplo Completo

```python
import wfdb
from ecg_plotter import ECGPlotter

# Carrega o arquivo ECG
record = wfdb.rdrecord('/caminho/para/o/arquivo')

# Cria uma instância da classe ECGPlotter
ecg_plotter = ECGPlotter(record, num_parts=12, samples_per_part=5000)

# Gera os gráficos dos segmentos e salva os dados
ecg_plotter.plot_segments()

# Calcula as métricas e salva em um arquivo JSON
ecg_plotter.calculate_metrics()
```

## Arquivos Gerados

- **ecg_graph_data.json**: Contém os dados dos gráficos dos segmentos do sinal ECG.
- **ecg_metrics.json**: Contém as métricas calculadas a partir do sinal ECG, como a frequência cardíaca, amplitude dos picos R, variabilidade da frequência cardíaca, entre outras.

## Contribuindo

Se você deseja contribuir para este projeto, por favor, siga os seguintes passos:

1. Faça um fork deste repositório.
2. Crie uma nova branch (`git checkout -b feature/nova-feature`).
3. Faça suas modificações e commit (`git commit -am 'Adicionando nova feature'`).
4. Envie para o repositório remoto (`git push origin feature/nova-feature`).
5. Abra um pull request.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
