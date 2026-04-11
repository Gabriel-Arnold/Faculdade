package up.desen.software.trabalho.main;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

import up.desen.software.trabalho.classes.Estabelecimento;
import up.desen.software.trabalho.classes.Itens;
import up.desen.software.trabalho.classes.Pedido;
import up.desen.software.trabalho.classes.Produto;
import up.desen.software.trabalho.classes.Usuario;
import up.desen.software.trabalho.enums.Status;

public class Main {
	
	private static ArrayList<Estabelecimento> Estabelecimentos = new ArrayList<Estabelecimento>();
	private static ArrayList<Pedido> Pedidos = new ArrayList<Pedido>();
	private static ArrayList<Usuario > usuarios = new ArrayList<Usuario>();
	private static Boolean Padrao = false;
	
	public static void main (String args[]) {
		Scanner sc = new Scanner(System.in);
		
		int select = -1;
		
		do {
			System.out.println("\n===============================");
			System.out.println("1 - Acessar painel do cliente.");
			System.out.println("2 - Acessar painel do administrador.");
			System.out.println("3 - Cadastrar dados padrões.");
			System.out.println("0 - Sair do programa.");
			System.out.println("===============================");
			
			System.out.println("\nDigite a opção que deseja: ");
			select = sc.nextInt();
			sc.nextLine();
			
			switch (select) {
			case 1: {
				Usuario user = Login_Cadastro_Usuario(sc);
				if(user != null) Painel_User(sc, user);
				continue;
			}
			case 2: {
				Painel_Admin(sc);
				continue;
			}
			case 3: {
				
				if(Padrao == true) {
					System.out.println("Dados padrão já estão cadastrados.");
					continue;
				}
				
				// Usuario
				
				int id = 0;
				for(Usuario user : usuarios) {
					if(id <= user.getID()) id = user.getID();
				}
				id++;
				usuarios.add(new Usuario(id, "joao", "123", "João da Silva", "Rua porto velho, 123 W"));
				
				// Estabelecimento
				
				id = 0;
				for(Estabelecimento estab : Estabelecimentos) {
					if(id <= estab.getID()) id = estab.getID();
				}
				id++;
				Estabelecimento estabelecimento = new Estabelecimento(id, "Café do Jorge");
				
				// Produtos
				
				estabelecimento.addProduto("Pão de Queijo", 3.0);
				estabelecimento.addProduto("Café", 4.90);
				
				Estabelecimentos.add(estabelecimento);
				
				System.out.println("Dados Padrões cadastrados.");
				System.out.println("Cliente - Usuario: joao, Senha: 123");
				System.out.println("Estabelecimento - Café do Jorge, Id: " + id + ".");
				
				Padrao = true;
				continue;
			}
			case 0: {
				System.out.println("\nObrigado pela preferência.");
			}
			default:
				System.out.println("\nOpção selecionada invalida.");;
			}
		}while(select != 0);
		
		sc.close();
	}
	
	private static void Painel_User(Scanner sc, Usuario user) {
		int select = -1;
		do {
			System.out.println("\n==========[ CLIENTE ]==========");
			System.out.println("1 - Fazer pedido.");
			System.out.println("2 - Vizualizar status do pedido.");
			System.out.println("0 - Voltar");
			System.out.println("===============================");
			System.out.println("\nSelecione a opção desejada:");
			
			select = sc.nextInt();
			sc.nextLine();
			
			switch (select) {
			case 1: {
				Fazer_Pedido(sc, user);
				continue;
			}
			case 2: {
				Status_Pedido(user);
				continue;
			}
			case 0: {
				return;
			}
			default:
				System.out.println("\nOpção selecionada invalida.");;
			}
		}while(select != 0);
	}
	
	private static void Painel_Admin(Scanner sc) {
		int select = -1;
		do {
			System.out.println("\n==========[ ADMINISTRADOR ]==========");
			System.out.println("1 - Cadastrar novo Estabelecimento.");
			System.out.println("2 - Excluir Estabelecimento.");
			System.out.println("3 - Gerenciar Estabelecimento.");
			System.out.println("4 - Listar Estabelecimentos.");
			System.out.println("5 - Listar Pedidos.");
			System.out.println("6 - Listar Usuarios.");
			System.out.println("7 - Mudar status do pedido.");
			System.out.println("0 - Voltar.");
			System.out.println("===============================");
			System.out.println("\nSelecione a opção desejada:");
			
			select = sc.nextInt();
			sc.nextLine();
			
			switch (select) {
			case 1: {
				cadastrasEstabelecimento(sc);
				continue;
			}
			case 2: {
				excluirEstabelecimento(sc);
				continue;
			}
			case 3: {
				gerenciarEstabelecimento(sc);
				continue;
			}
			case 4: {
				listarEstabelecimentos();
				continue;
			}
			case 5: {
				if(Pedidos.size() > 0) {
					System.out.println("ID - Cliente - Estabelecimento - Status");
					for(Pedido pedido : Pedidos) {
						System.out.println(pedido.getID() + " - " + pedido.getCliente().getNome() + " - " + pedido.getEstabelecimento().getNome() + " - " + Status_Pedido(pedido));
					}
				} else {
					System.out.println("Nenhum pedido feito.");
				}
				continue;
			}
			case 6: {
				if(usuarios.size() > 0) {
					System.out.println("ID - Usuario - Nome");
					for(Usuario user : usuarios) {
						System.out.println(user.getID() + " - " + user.getUsuario() + " - " + user.getNome());
					}
				} else {
					System.out.println("Nenhum usuario cadastrado.");
				}
				continue;
			}
			case 7: {
				System.out.println("Digite o id do pedido a ser alterado ou 0 para cancelar.");
				int id = sc.nextInt();
				sc.nextLine();
				if(id == 0) continue;
				Pedido pedido = null;
				for(Pedido p : Pedidos) {
					if(p.getID() == id) {
						pedido = p;
					}
				}
				if(pedido == null) {
					System.out.println("ID digitado inválido.");
					continue;
				} else {
					int status = -1;
					do {
						System.out.println("1 - Preparando");
						System.out.println("2 - Saiu para Entrega");
						System.out.println("3 - Finalizado");
						System.out.println("0 - Voltar");
						System.out.println("\n Digite qual status quer adicionar a este pedido: ");
						status = sc.nextInt();
						sc.nextLine();
						switch (status) {
						case 0: {
							break;
						}
						case 1: {
							pedido.setStatus(Status.Preparando);
							System.out.println("Status do pedido alterado para: Preparando.");
							status = 0;
							break;
						}
						case 2: {
							pedido.setStatus(Status.SaiuParaEntrega);
							System.out.println("Status do pedido alterado para: Saiu para Entrega.");
							status = 0;
							break;
						}
						case 3: {
							pedido.setStatus(Status.Finalizado);
							System.out.println("Status do pedido alterado para: Finalizado.");
							status = 0;
							break;
						}
						default:
							System.out.println("Valor digitado inválido.");
						}
					}while(status != 0);
				}
				continue;
			}
			case 0: {
				return;
			}
			default:
				System.out.println("\nOpção selecionada invalida.");;
			}
		}while(select != 0);
	}
	
	private static void Status_Pedido(Usuario user) {
		if(Pedidos.isEmpty()) {
			System.out.println("Você não tem pedidos.");
		} else {
			ArrayList<Pedido> pedidos_user = new ArrayList<Pedido>();
			for(Pedido p : Pedidos) {
				if(p.getCliente() == user) {
					pedidos_user.add(p);
				}
			}
			if(pedidos_user.isEmpty()) {
				System.out.println("Você não tem pedidos.");
			} else {
				System.out.println("Seus Pedidos: ");
				System.out.println("----------------------------------");
				for(Pedido p : pedidos_user) {
					System.out.println(p.getID() + " - " + p.getEstabelecimento().getNome() + " - " + Status_Pedido(p));
					System.out.println("Itens do pedido:");
					System.out.println("Produto - Quantidade - Valor unitário");
					Double total = 0.0;
					for(Itens item : p.getItens()) {
						System.out.println(item.getProduto().getNome() + " - " + item.getQuantidade() + " - R$ " + Formatar(item.getProduto().getPreco()));
						total = total + (item.getProduto().getPreco() * item.getQuantidade());
					}
					System.out.println("Total do pedido: R$ " + Formatar(total));
					System.out.println("----------------------------------");
				}
			}
		}
	}
	
	private static void Fazer_Pedido(Scanner sc, Usuario user) {
		int select = -1;
		Estabelecimento estab = null;
		do {
			for(Estabelecimento e : Estabelecimentos) {
				System.out.println(e.getID() + " - " + e.getNome());
			}
			System.out.println("Digite o id do estabelecimento ou 0 para voltar: ");
			select = sc.nextInt();
			sc.nextLine();
			for(Estabelecimento e : Estabelecimentos) {
				if(e.getID() == select) {
					estab = e;
					break;
				}
			}
			if(estab != null) break;
			System.out.println("Id digitado inválido.");
		}while(select != 0);
		if(estab == null) {
			System.out.println("ERRO: 1");
			return;
		}
		select = -1;
		Pedido pedido = new Pedido(0, user, estab);
		do {
			if(!pedido.getItens().isEmpty()) {
				System.out.println("\nItens no pedido: ");
				System.out.println(" Produto - Valor unitario - Quantidade - Valor total");
				Double total = 0.0;
				for(Itens item : pedido.getItens()) {
					total = total + (item.getProduto().getPreco() * item.getQuantidade());
					System.out.println(" " + item.getProduto().getNome() + " - R$" + Formatar(item.getProduto().getPreco()) + " - " + item.getQuantidade() + " - " + Formatar(item.getProduto().getPreco() * item.getQuantidade()));
				}
				System.out.println("Valor total do pedido: R$" + Formatar(total));
			}
			System.out.println("\nID - Produto - Preço unitario");
			HashMap<Integer, Produto> produtos = estab.getProdutos();
			for(int key : produtos.keySet()) {
				int id = key + 1;
				System.out.println(id + " - " + produtos.get(key).getNome() + " - R$" + Formatar(produtos.get(key).getPreco()));
			}
			System.out.println("0 - Voltar");
			System.out.println("1 - Continuar");
			System.out.println("\nDigite o id do item que quer adicionar ao pedido: ");
			select = sc.nextInt();
			sc.nextLine();
			
			if(select > 1) {
				int id = select;
				id--;
				if(produtos.containsKey(id)) {
					Produto produto = produtos.get(id);
					if(produto == null) {
						System.out.println("ERRO 1");
						continue;
					}
					if(!pedido.getItens().isEmpty()) {
						boolean contains = false;
						for(Itens item : pedido.getItens()) {
							if(item.getProduto() == produto) {
								contains = true;
								item.setQuantidade(item.getQuantidade() + 1);
							}
						}
						if(contains == false) {
							pedido.addItem(new Itens(produto, 1));
						}
						System.out.println("Item adicionado ao pedido.");
					} else {
						pedido.addItem(new Itens(produto, 1));
					}
				} else {
					System.out.println("Id digitado inválido.");
				}
			}
		}while(select != 0 && select != 1);
		
		select = -1;
		
		if(pedido.getItens().isEmpty()) {
			System.out.println("ERRO: 1");
			return;
		}
		
		do {
			System.out.println("\nResumo do pedido: ");
			System.out.println(" Produto - Valor unitario - Quantidade - Valor total");
			Double total = 0.0;
			for(Itens item : pedido.getItens()) {
				total = total + (item.getProduto().getPreco() * item.getQuantidade());
				System.out.println(" - " + item.getProduto().getNome() + " - R$" + Formatar(item.getProduto().getPreco()) + " - " + item.getQuantidade() + " - R$" + Formatar(item.getProduto().getPreco() * item.getQuantidade()));
			}
			System.out.println("Valor total do pedido: R$" + Formatar(total));
			
			System.out.println("0 - Cancelar pedido");
			System.out.println("1 - Confirmar pedido");
			
			select = Integer.parseInt(sc.nextLine());
			
			switch (select) {
			case 0: {
				System.out.println("Pedido cancelado.");
				return;
			}
			case 1: {
				System.out.println("Pedido realizado acompanhe o seu pedido pelo menu status do pedido.");
				int id = 0;
				if(Pedidos.isEmpty()) {
					id++;
					pedido.setID(id);
				} else {
					for(Pedido p : Pedidos) {
						if(id <= p.getID()) id = p.getID();
					}
					id++;
					pedido.setID(id);
				}
				pedido.setStatus(Status.Preparando);
				Pedidos.add(pedido);
				return;
			}
			default:
				System.out.println("Seleção inválida.");
				continue;
			}
		}while(select != 0);
	}
	
	private static Usuario Login_Cadastro_Usuario(Scanner sc) {
		int select = -1;
		do {
			System.out.println("===============================");
			System.out.println("1 - Logar em um usuario.");
			System.out.println("2 - Registrar um novo usuario.");
			System.out.println("3 - Listar usuarios.");
			System.out.println("0 - Para voltar.");
			System.out.println("===============================");
			System.out.println("Digite a opção desejada:");
			select = sc.nextInt();
			sc.nextLine();
			if(select > 0 && select <= 3) {
				break;
			} else {
				System.out.println("\nOpção selecionada invalida.");
			}
		}while(select !=0);
		if(select == 1) {
			String usuario;
			Usuario user = null;
			do {
				System.out.println("Digite o usuario ou digite sair para voltar:");
				usuario = sc.next();
				for(Usuario u : usuarios) {
					if(usuario.equalsIgnoreCase(u.getUsuario())) {
						user = u;
						usuario = "continue";
						break;
					}
				}
				if(usuario.equals("continue"))  {
					break;
				}
				System.out.println("Esse usuario não existe.");
			}while(!usuario.equalsIgnoreCase("sair"));
			if(usuario.equalsIgnoreCase("sair")) return null;
			if(user != null) {
				String senha;
				do {
					System.out.println("Digite a senha: ");
					senha = sc.next();
					if(user.getSenha().equals(senha)) {
						return user;
					}
					System.out.println("Senha incorreta.");
				}while(!senha.equalsIgnoreCase("sair"));
			} else {
				System.out.println("ERRO: 1");
				return null;
			}
		} else if(select == 2) {
			String usuario = null;
			do {
				System.out.println("Digite um nome de usuario: ");
				usuario = sc.next();
				sc.nextLine();
				for(Usuario user : usuarios) {
					if(!user.getUsuario().equals(usuario)) {
						continue;
					} else {
						System.out.println("Esse usuário já existe.");
						break;
					}
				}
				break;
			}while(!usuario.equalsIgnoreCase("sair"));
			if(usuario != null && !usuario.equalsIgnoreCase("sair")) {
				
				System.out.println("Digite o seu nome completo: ");
				String nome = null;
				nome = sc.nextLine();
				
				if(nome != null) {
					
					System.out.println("Digite o seu endereço: ");
					String endereco = null;
					endereco = sc.nextLine();
					
					if(endereco != null) {
						
						System.out.println("Digite uma senha: ");
						String senha = null;
						senha = sc.next();
						sc.nextLine();
						
						if(senha != null) {
							
							System.out.println(senha);
							
							int id = 0;
							
							for(Usuario user : usuarios) {
								if(id <= user.getID()) id = user.getID();
							}
							
							id++;
							Usuario user = new Usuario(id, usuario, senha, nome, endereco);
							usuarios.add(user);
							System.out.println("Usuario criado.");
							return null;
						} else {
							System.out.println("ERRO: 3");
							return null;
						}
					} else {
						System.out.println("ERRO: 2");
						return null;
					}
				} else {
					System.out.println("ERRO: 1");
					return null;
				}
			}
			return null;
		} else if(select == 3) {
			System.out.println("Usuarios cadastrados: ");
			System.out.println("ID - Usuario");
			for(Usuario user : usuarios) {
				System.out.println(user.getID() + " - " + user.getUsuario());
			}
		} else {
			System.out.println("ERRO: 1");
			return null;
		}
		return null;
	}
	
	private static void cadastrasEstabelecimento(Scanner sc) {
		String nome;
		int id = 0;
		
		for(Estabelecimento estab : Estabelecimentos) {
			if(id <= estab.getID()) id = estab.getID();
		}
		
		id++;
		
		System.out.println("\nDigite o nome do Estabelecimento: ");
		nome = sc.nextLine();
		
		Estabelecimento estabelecimento = new Estabelecimento(id, nome);
		Estabelecimentos.add(estabelecimento);
		
		System.out.println("Estabelecimento cadastrado.");
	}
	
	private static void gerenciarEstabelecimento(Scanner sc) {
		int id = -1;
		Estabelecimento estab = null;
		do {
			System.out.println("\nDigite o id do estabelecimento ou 0 para voltar: ");
			id = Integer.valueOf(sc.next());
			Boolean encontrado = false;
			for(Estabelecimento e : Estabelecimentos) {
				if(e.getID() == id) {
					estab = e;
					encontrado = true;
					break;
				}
			}
			if(encontrado) break;
			System.out.println("Nenhum estabelecimento cadastrado com esse id.");
		}while(id != 0);
		
		if(id == 0) return;
		if(estab == null) {
			System.out.println("ERRO: 1");
		}
		
		int select = -1;
		
		do {
			System.out.println("\nSelecione a opção desejada:");
			System.out.println("\n==========[ " + estab.getNome() + " ]==========");
			System.out.println("1 - Listar produtos.");
			System.out.println("2 - Cadastrar novo produto.");
			System.out.println("3 - Excluir produto.");
			System.out.println("4 - Gerenciar produto.");
			System.out.println("0 - Voltar.");
			System.out.println("===============================");
			
			System.out.println("\nDigite a opção que deseja: ");
			select = sc.nextInt();
			sc.nextLine();
			
			switch (select) {
			case 1: {
				estab.ListarProdutos();
				continue;
			}
			case 2: {
				System.out.println("Digite o nome do produto");
				String nome = sc.nextLine();
				System.out.println("Digite o preço do produto");
				Double preco = 0.0;
				do {
					preco = Double.parseDouble(sc.nextLine());
					if(preco <= 0) {
						System.out.println("O preço deve ser maior que 0");
					}
				}while(preco <= 0);
				estab.addProduto(nome, preco);
				System.out.println("Produto cadastrado.");
				continue;
			}
			case 3: {
				System.out.println("Digite o id do produto que deseja excluir:");
				int id_produto = sc.nextInt();
				sc.nextLine();
				estab.removerProduto(id_produto);
				continue;
			}
			case 4: {
				gerenciarProduto(sc, estab);
				continue;
			}
			case 0: {
				return;
			}
			default:
				System.out.println("Opção selecionada inválida.");;
			}
		} while(select != 0);
	}
	
	private static void gerenciarProduto(Scanner sc, Estabelecimento estab) {
		int id = -1;
		Produto produto = null;
		do {
			System.out.println("Digite o id do produto que quer gerenciar:");
			id = sc.nextInt();
			sc.nextLine();
			if(id > 0) {
				produto = estab.getProduto(id);
				break;
			}
		}while(id != 0);
		if(produto != null) {
			int select = -1;
			do {
				System.out.println("\nSelecione a opção desejada:");
				System.out.println("\n==========[ " + produto.getNome() + " ]==========");
				System.out.println("1 - Alterar nome.");
				System.out.println("2 - Alterar preço.");
				System.out.println("0 - Voltar.");
				System.out.println("===============================");
				
				System.out.println("\nDigite a opção que deseja: ");
				select = sc.nextInt();
				sc.nextLine();
				
				switch (select) {
				case 1: {
					System.out.println("Digite o nome do produto: ");
					String nome = sc.next();
					sc.nextLine();
					produto.setNome(nome);
					System.out.println("Nome do produto alterado para " + nome);
					continue;
				}
				case 2: {
					System.out.println("Digite o preço do produto: ");
					Double preco = 0.0;
					do {
						preco = sc.nextDouble();
						sc.nextLine();
						if(preco <= 0) {
							System.out.println("O preço deve ser maior que 0");
						}
					}while(preco <= 0);
					produto.setPreco(preco);
					System.out.println("O preço do produto foi alterado para: " + preco);
					continue;
				}
				case 0: {
					return;
				}
				default:
					System.out.println("Opção selecionada inválida.");
				}
				
			}while(select != 0);
		} else {
			System.out.println("ERRO: 1");
			return;
		}
	}
	
	private static void listarEstabelecimentos() {
		if(Estabelecimentos.isEmpty()) {
			System.out.println("Não há estabelecimentos cadastrados.");
			return;
		}
		System.out.println("\nEstabelecimentos cadastrados: ");
		System.out.println("ID - Nome");
		for(Estabelecimento e : Estabelecimentos) {
			System.out.println(e.getID() + " - " + e.getNome());
		}
	}
	
	private static void excluirEstabelecimento(Scanner sc) {
		System.out.println("Digite o id do estabelecimento que deseja excluir: ");
		int id = sc.nextInt();
		sc.nextLine();
		Estabelecimento estab = null;
		for(Estabelecimento e : Estabelecimentos) {
			if(e.getID() == id) {
				estab = e;
			}
		}
		if(estab != null) {
			System.out.println("Tem certeza que quer excluir o estabeleciomento " + estab.getNome());
			System.out.println("Digite 1 para excluir ou 0 para cancelar:");
			int select = -1;
			do {
				select = sc.nextInt();
				sc.nextLine();
				if(select == 1) {
					Estabelecimentos.remove(estab);
					System.out.println("Estabeleciomento excluido.");
					return;
				} else if(select == 0) {
					return;
				}
				System.out.println("Valor digitado inválido.");
			}while (select != 0);
		} else {
			System.out.println("Estabelecimento não encontrado.");
		}
	}
	
	private static String Status_Pedido(Pedido p) {
		String status = "";
		if(p.getStatus() == Status.Preparando) {
			status = "Preparando";
		}else if(p.getStatus() == Status.SaiuParaEntrega) {
			status = "Saiu para Entrega";
		}else if(p.getStatus() == Status.Finalizado) {
			status = "Finalizado";
		}
		return status;
	}
	
	private static String Formatar(Double d) {
		DecimalFormat format = new DecimalFormat("##.00");
		return format.format(d);
	}

}
