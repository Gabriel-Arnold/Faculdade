package gabrieldev.com.br.commands;

import java.nio.charset.StandardCharsets;
import java.util.List;

import org.bukkit.ChatColor;
import org.bukkit.Material;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.entity.Player;
import org.bukkit.inventory.ItemStack;
import org.bukkit.inventory.meta.BookMeta;

import gabrieldev.com.br.cripto.CryptoService;
import gabrieldev.com.br.cripto.EncryptedData;
import gabrieldev.com.br.helpers.BookHelper;

public class Cofre implements CommandExecutor {

	@SuppressWarnings("deprecation")
	@Override
	public boolean onCommand(CommandSender sender, Command cmd, String lb, String[] args) {
		if(!(sender instanceof Player)) return false;
		if(cmd.getName().equalsIgnoreCase("cofre")) {
			Player p = (Player) sender;
			if(args.length < 1) {
				Help(p);
				return false;
			}
			switch (args[0].toLowerCase()) {
			case "cifrar": {
				if (args.length < 2) {
					p.sendMessage(ChatColor.RED + "/cofre cifrar (senha)");
					return false;
				}
				
				ItemStack item = p.getItemInHand();
				
				if(item.getType() != Material.WRITABLE_BOOK) {
					p.sendMessage(ChatColor.RED + "Você precisa ter um livro na mão.");
					return false;
				}
				
				BookMeta meta = (BookMeta) item.getItemMeta();
				List<String> paginas = meta.getPages();
				
				if(paginas == null || paginas.isEmpty()) {
					p.sendMessage(ChatColor.RED + "O livro está vazio.");
					return false;
				}
				
				String texto = String.join("\n", paginas);
				String senha = args[1];
				
				try {
					byte[] txt = texto.getBytes(StandardCharsets.UTF_8);
                    EncryptedData data = CryptoService.encrypt(txt, senha);
                    
                    p.getInventory().addItem(BookHelper.getBook(data));

                    p.sendMessage(ChatColor.GREEN + "Livro cifrado com sucesso.");
				} catch (Exception e) {
					e.printStackTrace();
				}
				return true;
				
			}
			case "decifrar": {
				if (args.length < 2) {
					p.sendMessage(ChatColor.RED + "/cofre decifrar (senha)");
					return false;
				}
				
				ItemStack item = p.getItemInHand();
				
				if(item.getType() != Material.WRITTEN_BOOK) {
					p.sendMessage(ChatColor.RED + "Você precisa estar com um livro cifrado na mão.");
					return false;
				}
				if(!(item.getItemMeta() instanceof BookMeta)) {
					p.sendMessage(ChatColor.RED + "Esse item não é um livro válido.");
					return false;
				}
				
				BookMeta meta = (BookMeta) item.getItemMeta();
				
				if(!(BookHelper.isEncryptedBook(meta))) {
					p.sendMessage(ChatColor.RED + "Esse livro não está cifrado.");
					return false;
				}
				
				String senha = args[1];
				
				try {
					EncryptedData data = BookHelper.read(meta);
					
					byte[] textoByte = CryptoService.decrypt(data.getSalt(), data.getIv(), data.getCiphertext(), senha);
					String texto = new String(textoByte, StandardCharsets.UTF_8);
					
					p.getInventory().addItem(BookHelper.getNormalBook(texto));
					p.sendMessage(ChatColor.GREEN + "Livro decifrado com sucesso.");
				} catch (Exception e) {
					p.sendMessage(ChatColor.RED + "Erro ao decifrar. Senha incorreta ou conteudo corrompido.");
					e.printStackTrace();
				}
				return true;
			}
			default:
				Help(p);
			}
		}
		return false;
	}
	
	private void Help(Player p) {
		p.sendMessage(ChatColor.YELLOW + "/cofre cifrar (senha)");
		p.sendMessage(ChatColor.YELLOW + "/cofre decifrar (senha)");
	}

}
