package gabrieldev.com.br.main;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.plugin.java.JavaPlugin;

import gabrieldev.com.br.commands.Cofre;

public class Main extends JavaPlugin {
	
	@Override
	public void onEnable() {
		getCommand("cofre").setExecutor(new Cofre());
		Bukkit.getConsoleSender().sendMessage(ChatColor.GREEN + "Plugin iniciado.");
	}
	
	@Override
	public void onDisable() {
		// TODO Auto-generated method stub
		super.onDisable();
	}

}
