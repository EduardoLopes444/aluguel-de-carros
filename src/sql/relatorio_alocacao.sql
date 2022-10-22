select i.data_saida
     , i.data_entrega
     , i.chassi
     , i.cpf
     , i.valor_diaria

  from itens_pedido i
  inner join clientes c
  on i.cpf = c.cpf
  inner join categoria cat
  on i.valor_diaria = cat.valor_diaria
  inner join carro car
  on i.chassi = car.chassi
 order by i.cpf