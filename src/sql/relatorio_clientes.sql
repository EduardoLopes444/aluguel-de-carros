select c.cpf
     , c.rg 
     , c.data_nascimento 
     , c.cnh 
     , c.nome 
     , c.endereco 
  from clientes c
 order by c.nome