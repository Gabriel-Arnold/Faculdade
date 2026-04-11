package up.desen.software.trabalho.classes;

public class Produto {
	
	private String NOME;
	private Double PRECO;
	
	public Produto(String nome, Double preco) {
		this.NOME = nome;
		this.PRECO = preco;
	}
	
	public void setNome(String nome) {
		this.NOME = nome;
	}
	
	public void setPreco(Double preco) {
		this.PRECO = preco;
	}
	
	public String getNome() {
		return this.NOME;
	}
	
	public Double getPreco() {
		return this.PRECO;
	}

}
