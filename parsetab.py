
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '|\x84N\xe6\x0f\x0e\xfd\x956B\xe5\xe2\xb3\\\x08\xdc'
    
_lr_action_items = {'IS':([10,24,],[15,30,]),'USE':([0,],[1,]),'END':([22,29,34,41,54,70,],[28,-12,-11,55,-31,-30,]),'ASSIGN_OP':([58,59,60,],[72,-28,-29,]),'SEMICOLON':([8,17,18,23,26,38,39,40,42,45,46,47,49,53,56,59,60,62,71,73,75,],[13,-5,-6,29,34,51,52,54,-33,61,62,63,68,69,-32,-28,-29,-19,74,-22,77,]),'GENERIC':([15,],[19,]),'OF':([11,],[16,]),'DECIMAL':([8,9,17,18,],[12,14,-5,-6,]),'ENTITY':([0,28,],[6,39,]),'PORT':([15,20,61,],[21,21,-13,]),'COLON':([32,36,50,68,],[44,48,-24,-23,]),'COMMA':([31,32,37,58,59,60,76,],[43,-16,50,-17,-28,-29,-18,]),'ARCHITECTURE':([0,55,],[7,71,]),'LPAREN':([19,21,],[25,27,]),'IN':([48,],[65,]),'RPAREN':([31,32,33,35,51,57,58,59,60,63,76,],[-15,-16,45,46,-21,-14,-17,-28,-29,-20,-18,]),'BIT':([44,64,65,66,67,],[59,-27,-25,59,-26,]),'OUT':([48,],[67,]),'ID':([1,6,7,12,14,16,25,27,30,35,36,39,42,43,44,50,51,54,63,64,65,66,67,68,71,72,],[9,10,11,17,18,24,32,37,42,37,49,53,42,32,60,-24,-21,42,-20,-27,-25,60,-26,-23,75,76,]),'INOUT':([48,],[64,]),'$end':([2,3,4,5,13,52,69,74,77,],[-2,-1,0,-3,-4,-7,-8,-9,-10,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'generic_decl':([15,],[20,]),'portdir':([48,],[66,]),'arch_expressions':([30,42,54,],[40,56,40,]),'portlist':([27,],[35,]),'portnames':([27,35,],[36,36,]),'generic_stmt':([25,43,],[31,31,]),'library':([1,],[8,]),'entity':([0,],[2,]),'header':([0,],[3,]),'entity_body':([15,],[22,]),'design':([0,],[4,]),'architecture':([0,],[5,]),'porttype':([44,66,],[58,73,]),'architecture_body':([30,54,],[41,70,]),'ports':([15,20,],[23,26,]),'generic_stmts':([25,43,],[33,57,]),'portdecl':([27,35,],[38,47,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> design","S'",1,None,None,None),
  ('design -> header','design',1,'p_design','/home/dilawar/Works/github/pyghdl/language/vhdl.py',89),
  ('design -> entity','design',1,'p_design','/home/dilawar/Works/github/pyghdl/language/vhdl.py',90),
  ('design -> architecture','design',1,'p_design','/home/dilawar/Works/github/pyghdl/language/vhdl.py',91),
  ('header -> USE library SEMICOLON','header',3,'p_header','/home/dilawar/Works/github/pyghdl/language/vhdl.py',95),
  ('library -> library DECIMAL ID','library',3,'p_library','/home/dilawar/Works/github/pyghdl/language/vhdl.py',98),
  ('library -> ID DECIMAL ID','library',3,'p_library','/home/dilawar/Works/github/pyghdl/language/vhdl.py',99),
  ('entity -> ENTITY ID IS entity_body END ENTITY SEMICOLON','entity',7,'p_entity','/home/dilawar/Works/github/pyghdl/language/vhdl.py',102),
  ('entity -> ENTITY ID IS entity_body END ENTITY ID SEMICOLON','entity',8,'p_entity','/home/dilawar/Works/github/pyghdl/language/vhdl.py',103),
  ('architecture -> ARCHITECTURE ID OF ID IS architecture_body END ARCHITECTURE SEMICOLON','architecture',9,'p_architecture','/home/dilawar/Works/github/pyghdl/language/vhdl.py',107),
  ('architecture -> ARCHITECTURE ID OF ID IS architecture_body END ARCHITECTURE ID SEMICOLON','architecture',10,'p_architecture','/home/dilawar/Works/github/pyghdl/language/vhdl.py',108),
  ('entity_body -> generic_decl ports SEMICOLON','entity_body',3,'p_entity_body','/home/dilawar/Works/github/pyghdl/language/vhdl.py',112),
  ('entity_body -> ports SEMICOLON','entity_body',2,'p_entity_body','/home/dilawar/Works/github/pyghdl/language/vhdl.py',113),
  ('generic_decl -> GENERIC LPAREN generic_stmts RPAREN SEMICOLON','generic_decl',5,'p_generic_decl','/home/dilawar/Works/github/pyghdl/language/vhdl.py',117),
  ('generic_stmts -> generic_stmt COMMA generic_stmts','generic_stmts',3,'p_generic_stmts','/home/dilawar/Works/github/pyghdl/language/vhdl.py',120),
  ('generic_stmts -> generic_stmt','generic_stmts',1,'p_generic_stmts','/home/dilawar/Works/github/pyghdl/language/vhdl.py',121),
  ('generic_stmt -> ID','generic_stmt',1,'p_generic_stmt','/home/dilawar/Works/github/pyghdl/language/vhdl.py',125),
  ('generic_stmt -> ID COLON porttype','generic_stmt',3,'p_generic_stmt','/home/dilawar/Works/github/pyghdl/language/vhdl.py',126),
  ('generic_stmt -> ID COLON porttype ASSIGN_OP ID','generic_stmt',5,'p_generic_stmt','/home/dilawar/Works/github/pyghdl/language/vhdl.py',127),
  ('ports -> PORT LPAREN portlist RPAREN SEMICOLON','ports',5,'p_ports','/home/dilawar/Works/github/pyghdl/language/vhdl.py',131),
  ('portlist -> portlist portdecl SEMICOLON','portlist',3,'p_portlist','/home/dilawar/Works/github/pyghdl/language/vhdl.py',134),
  ('portlist -> portdecl SEMICOLON','portlist',2,'p_portlist','/home/dilawar/Works/github/pyghdl/language/vhdl.py',135),
  ('portdecl -> portnames COLON portdir porttype','portdecl',4,'p_portdecl','/home/dilawar/Works/github/pyghdl/language/vhdl.py',139),
  ('portnames -> portnames ID SEMICOLON','portnames',3,'p_portnames','/home/dilawar/Works/github/pyghdl/language/vhdl.py',142),
  ('portnames -> ID COMMA','portnames',2,'p_portnames','/home/dilawar/Works/github/pyghdl/language/vhdl.py',143),
  ('portdir -> IN','portdir',1,'p_portdir','/home/dilawar/Works/github/pyghdl/language/vhdl.py',147),
  ('portdir -> OUT','portdir',1,'p_portdir','/home/dilawar/Works/github/pyghdl/language/vhdl.py',148),
  ('portdir -> INOUT','portdir',1,'p_portdir','/home/dilawar/Works/github/pyghdl/language/vhdl.py',149),
  ('porttype -> BIT','porttype',1,'p_porttype','/home/dilawar/Works/github/pyghdl/language/vhdl.py',153),
  ('porttype -> ID','porttype',1,'p_porttype','/home/dilawar/Works/github/pyghdl/language/vhdl.py',154),
  ('architecture_body -> arch_expressions SEMICOLON architecture_body','architecture_body',3,'p_architecture_body','/home/dilawar/Works/github/pyghdl/language/vhdl.py',158),
  ('architecture_body -> arch_expressions SEMICOLON','architecture_body',2,'p_architecture_body','/home/dilawar/Works/github/pyghdl/language/vhdl.py',159),
  ('arch_expressions -> ID arch_expressions','arch_expressions',2,'p_arch_expressions','/home/dilawar/Works/github/pyghdl/language/vhdl.py',162),
  ('arch_expressions -> ID','arch_expressions',1,'p_arch_expressions','/home/dilawar/Works/github/pyghdl/language/vhdl.py',163),
]
