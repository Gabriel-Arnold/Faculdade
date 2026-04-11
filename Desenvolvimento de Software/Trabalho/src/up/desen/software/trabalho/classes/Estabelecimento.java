package up.desen.software.trabalho.classes;

import java.util.HashMap;

public class Estabelecimento {
	
	private int ID;
	private String NOME;
	private HashMap<Integer, Produto> PRODUTOS;
	
	public Estabelecimento(int id, String nome) {
		this.ID = id;
		this.NOME = nome;
		this.PRODUTOS = new HashMap<Integer, Produto>();
	}
	
	public void setID(int id) {
		this.ID = id;
	}
	
	public void setString(String nome) {
		this.NOME = nome;
	}
	
	public void addProduto(String nome, Double preco) {
		int id = 0;
		if(!(PRODUTOS.isEmpty())) {
			for(int key : PRODUTOS.keySet()) {
				if(id <= key) id = key;
			}
		}
		id++;
		Produto prod = new Produto(nome, preco);
		PRODUTOS.put(id, prod);
		System.out.println("Produto cadastrado com o id: " + id);
	}
	
	public void removerProduto(int id) {
		if(!PRODUTOS.isEmpty()) {
			if(id > 0) {
				if(PRODUTOS.containsKey(id)) {
					PRODUTOS.remove(id);
					System.out.println("Produto removido.");
				} else {
					System.out.println("Esse produto não existe.");
				}
			} else {
				System.out.println("ID inválido.");
			}
		} else {
			System.out.println("Não há produtos cadastrados.");
		}
	}
	
	public Produto getProduto(int id) {
		if(!PRODUTOS.isEmpty()) {
			if(id > 0) {
				if(PRODUTOS.containsKey(id)) {
					return PRODUTOS.get(id);
				} else {
					System.out.println("Esse produto não existe.");
				}
			} else {
				System.out.println("ID inválido.");
			}
		} else {
			System.out.println("Não há produtos cadastrados.");
		}
		return null;
	}
	
	public HashMap<Integer, Produto> getProdutos() {
		return this.PRODUTOS;
	}
	
	
	public int getID() {
		return this.ID;
	}
	
	public String getNome() {
		return this.NOME;
	}
	
	public void ListarProdutos() {
		System.out.println("\nProdutos Cadastrados:");
		System.out.println("\nID - Produto - Valor");
		for(int key : PRODUTOS.keySet()) {
			System.out.println("" + key + " - " + PRODUTOS.get(key).getNome() + " - " + PRODUTOS.get(key).getPreco());
		}
	}

}
