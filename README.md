## holidays_co

Portado a módulo de Python desde [colombia-holidays](https://github.com/nequibc/colombia-holidays)

Días festivos no laborables en Colombia. Calculados con base en la ley 51 de 1983

**Última vez modificado**: 2019-06-30   
**Desde**: 2019-06-29   
**Version**: 0.0.2    
**Autor:** Javier Mejía <_jmjaviermejiaest@gmail.com_>

### Instalación
```shell
$ pip install holidays_co
```
### Ejemplo
```python
import holidays_co
holidays = holidays_co.get_colombia_holidays_by_year(2019)
```
o
```python
from holidays_co import get_colombia_holidays_by_year
holidays = get_colombia_holidays_by_year(2019)
```
---
#### Métodos disponibles
- **get_colombia_holidays_by_year(year)**: Devuelve la lista de festivos no laborables en Colombia para un año

    _Input_: `type(int)`    
    _Output_: `list(namedtuple("Holiday", ["date", "celebration"]))`
- **is_holiday_date(date)**: Returna `True`, si la fecha ingresada corresponde a un día festivo, `False` en caso contrario.     
    _Input_: `type(date)`   
    _Output_: `type(bool)`
