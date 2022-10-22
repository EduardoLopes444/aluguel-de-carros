select car.chassi
     , car.cor 
     , car.modelo 
     , car.marca 
     , car.placa 
     , car.ano 
     , cat.codigo_categoria
     , cat.valor_diaria
  from carro car
  inner join categoria cat
  on cat.codigo_categoria = car.codigo_categoria
 order by car.chassi