package gabrieldev.com.br.helpers;

import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

import org.bukkit.Material;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.BookMeta;

import gabrieldev.com.br.cripto.EncryptedData;

public class BookHelper {
	
	public static ItemStack getBook(EncryptedData data) {
		ItemStack item = new ItemStack(Material.WRITTEN_BOOK);
		BookMeta meta = (BookMeta) item.getItemMeta();
		
		String salt = Base64.getEncoder().encodeToString(data.getSalt());
		String iv = Base64.getEncoder().encodeToString(data.getIv());
		String ct = Base64.getEncoder().encodeToString(data.getCiphertext());
		
		StringBuilder content = new StringBuilder();
		content.append("SALT: ").append(salt).append("\n");
		content.append("IV: ").append(iv).append("\n");
		content.append("CT: ").append(ct).append("\n");
		
		List<String> paginas = splitPages(content.toString(), 220);
		
		meta.setTitle("Livro Cifrado");
		meta.setAuthor("Cofre");
		meta.setPages(paginas);
		
		item.setItemMeta(meta);
		return item;
	}
	
	public static ItemStack getNormalBook(String text) {
		ItemStack item = new ItemStack(Material.WRITTEN_BOOK);
		BookMeta meta = (BookMeta) item.getItemMeta();
		
		List<String> paginas = splitPages2(text, 220);
		
		meta.setPages(paginas);
		meta.setTitle("Texto decriptografado.");
		meta.setAuthor("Cofre");
		
		item.setItemMeta(meta);
		return item;
	}
	
	public static boolean isEncryptedBook(BookMeta meta) {
		if(meta == null || meta.getPages() == null || meta.getPages().isEmpty()) return false;
		
		String content = String.join("", meta.getPages());
		return content.startsWith("SALT: ");
	}
	
	public static EncryptedData read(BookMeta meta) {
		if(!(isEncryptedBook(meta))) throw new IllegalArgumentException("Livro está no formato errado.");
		
		List<String> pages = meta.getPages();
		String content = String.join("", pages);
		
		String[] linhas = content.split("\n");
		
		String salt64 = null;
		String iv64 = null;
		String ct64 = null;
		
		for(String linha : linhas) {
			if(linha.startsWith("SALT: ")) salt64 = linha.substring("SALT: ".length());
			if(linha.startsWith("IV: ")) iv64 = linha.substring("IV: ".length());
			if(linha.startsWith("CT: ")) ct64 = linha.substring("CT: ".length());
		}
		
		if(salt64 == null || iv64 == null || ct64 == null) throw new IllegalArgumentException("Dados incompletos no livro.");
		
		byte[] salt = Base64.getDecoder().decode(salt64);
		byte[] iv = Base64.getDecoder().decode(iv64);
		byte[] ct = Base64.getDecoder().decode(ct64);
		
		return new EncryptedData(salt, iv, ct);
	}
	
	private static List<String> splitPages(String text, int maxCharsPerPage) {
		List<String> pages = new ArrayList<String>();
		for(int i = 0; i < text.length(); i += maxCharsPerPage) {
			int end = Math.min(i + maxCharsPerPage, text.length());
			pages.add(text.substring(i, end));
		}
		
		if(pages.isEmpty()) {
			pages.add("");
		}
		
		return pages;
	}
	
	private static List<String> splitPages2(String text, int maxCharsPerPage) {
		List<String> pages = new ArrayList<String>();
		
		if(text == null || text.isEmpty()) {
			pages.add("");
			return pages;
		}
		
		for(int i = 0; i < text.length(); i += maxCharsPerPage) {
			int end = Math.min(i + maxCharsPerPage, text.length());
			pages.add(text.substring(i, end));
		}
		
		return pages;
	}

}
