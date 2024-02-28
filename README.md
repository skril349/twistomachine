

## Funcionalitats

El script principal `main.py` realitza les següents tasques:

- **TkInter**: Permet realitzar una interfície gràfica per controlar el sistema.
- **Tracció**: introduïnt paràmetres de pause1, distancia1, pause2, distancia2, cicles i triggers, podem realitzar un cicle complert de tracció.
- **Rotació**: introduïnt paràmetres de pause, cicles i posicions, podem realitzar un cicle complert de rotació generant triggers a time = pause/2.
- **Tracció i rotació**: introduïnt valors de pause, Dx, N i Triggersm podem generar un gràfic complert de tracció i rotació.

## Com Utilitzar

Per executar el script `main.py`, es important tenir connectat a l'ordinador tant l'electrònica de Odrive com la de Arduino, i seleccionar a la carpeta >Odrive>odrive_setup.py quin es el port COM del Arduino.
Podeu utilitzar diferents arguments de línia de comandes per executar tasques específiques:

Es pot crear un entorn virtual si es vol ( no necessari):
```
virtualenv venv
```

Posteriorment instalarem els requeriments necessaris:
```
pip install -r requirements.txt
```
L'execució del codi es farà de la següent manera:

- **root**: Accedim a la carpeta principal del projecte.
    ```
    python main.py
    ```

### Tests
Els tests es poden executar mitjançant el següent comandament:
```
cd Tests
```

- **test_json_structure.py**: Genera l'estructura de fitxers que el codi espera.
```
python test_json_structure.py
```
- **test_traction.py**: Genera una seqüència de tracció.
```
python test_traction.py
```

- **test_twisting.py**: Genera una seqüència de torsió.
```
python test_twisting.py
```

- **testing_odrive.py**: Genera una seqüència de twisting i traction.
```
python testing_odrive.py
```