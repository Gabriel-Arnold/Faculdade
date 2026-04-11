package up.desen.software.trabalho.classes;

public class Itens {
	
	private Produto PRODUTO;
	private int QUANTIDADE;
	
	public Itens(Produto produto, int quantidade) {
		this.PRODUTO = produto;
		this.QUANTIDADE = quantidade;
	}
	
	public void setProduto(Produto produto) {
		this.PRODUTO = produto;
	}
	
	public void setQuantidade(int quantidade) {
		this.QUANTIDADE = quantidade;
	}
	
	public Produto getProduto() {
		return this.PRODUTO;
	}
	
	public int getQuantidade() {
		return this.QUANTIDADE;
	}

}
