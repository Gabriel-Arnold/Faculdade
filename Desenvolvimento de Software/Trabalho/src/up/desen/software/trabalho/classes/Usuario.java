package up.desen.software.trabalho.classes;

public class Usuario {
	
	private int ID;
	private String USUARIO;
	private String SENHA;
	private String NOME;
	private String ENDERECO;
	
	public Usuario(int id, String usuario, String senha, String nome, String endereco) {
		this.ID = id;
		this.USUARIO = usuario;
		this.SENHA = senha;
		this.NOME = nome;
		this.ENDERECO = endereco;
	}
	
	public void setID(int id) {
		this.ID = id;
	}
	
	public void setUsuario(String usuario) {
		this.USUARIO = usuario;
	}
	
	public void setSenha(String senha) {
		this.SENHA = senha;
	}
	
	public void setNome(String nome) {
		this.NOME = nome;
	}
	
	public void setEndereco(String endereco) {
		this.ENDERECO = endereco;
	}
	
	public int getID() {
		return this.ID;
	}
	
	public String getUsuario() {
		return this.USUARIO;
	}
	
	public String getSenha() {
		return this.SENHA;
	}
	
	public String getNome() {
		return this.NOME;
	}
	
	public String getEndereco() {
		return this.ENDERECO;
	}

}
