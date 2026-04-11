package up.desen.software.trabalho.classes;

import java.util.ArrayList;

import up.desen.software.trabalho.enums.*;

public class Pedido {
	
	private int ID;
	private Usuario CLIENTE;
	private Estabelecimento ESTABELECIMENTO;
	private Status STATUS;
	private ArrayList<Itens> ITENS = new ArrayList<Itens>();
	
	public Pedido(int id, Usuario cliente, Estabelecimento Estabelecimento) {
		this.ID = id;
		this.CLIENTE = cliente;
		this.ESTABELECIMENTO = Estabelecimento;
	}
	
	public void setID(int id) {
		this.ID = id;
	}
	
	public void setCliente(Usuario user) {
		this.CLIENTE = user;
	}
	
	public void setEstabelecimento(Estabelecimento estabelecimento) {
		this.ESTABELECIMENTO = estabelecimento;
	}
	
	public void setStatus(Status status) {
		this.STATUS = status;
	}
	
	public int getID() {
		return this.ID;
	}
	
	public Usuario getCliente() {
		return this.CLIENTE;
	}
	
	public Estabelecimento getEstabelecimento() {
		return this.ESTABELECIMENTO;
	}
	
	public Status getStatus() {
		return this.STATUS;
	}
	
	public ArrayList<Itens> getItens() {
		return this.ITENS;
	}
	
	public void addItem(Itens item) {
		this.ITENS.add(item);
	}

}
