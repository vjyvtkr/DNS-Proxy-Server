import java.io.*;
import java.net.*;
import java.util.*;

public class DNSProxyServer{

	//Constant Variables and a HashMap
	public static final int ARRAY_SIZE = 512;
	public static int CACHE_SIZE;
	public static int PORT;
	public static String NS_IP;
	public static final int HASH_SIZE = 510;
	public static final int STD_NS_PORT = 53;
	public static HashMap<String, byte[]> proxy;
	public static HashMap<Integer, String> recent;

	public static void main(String[] args) throws IOException{

		if(args.length!=3){
			System.out.println("Usage: java DNSProxyServer 'IP' Port'' 'Cache Size'\nLook at README.");
			System.exit(1);
		}

		//Set Cache_Size
		NS_IP = args[0];
		PORT = Integer.parseInt(args[1]);
		CACHE_SIZE = Integer.parseInt(args[2]);

		//Hashmap storing most recent entries.  (No. of recent entries = cache_size)
		recent = new HashMap<Integer, String>();

		//HashMap which stores request and response without the querieID.
		proxy = new HashMap<String, byte[]>();                           

		//ServerSocket for input from terminal created on port 6969
		DatagramSocket serverSocket = new DatagramSocket(PORT);
		int entries=0;
		while(true){
			System.out.println("Proxy Server Listening\n");

			//Datagram packet received from terminal.
			byte[] receivedData = new byte[ARRAY_SIZE];       				
			DatagramPacket clientRequest = new DatagramPacket(receivedData, receivedData.length);


			serverSocket.receive(clientRequest);

			//Get terminal IP and Port
			InetAddress termIP = clientRequest.getAddress();
			int termPort = clientRequest.getPort();

			//Remove the query ID (first and second byte) and store the request in a byte array and convert to string.
			byte[] keyForHM = new byte[HASH_SIZE];
			int k=0;
			for(int i=2; i<receivedData.length; i++){
				keyForHM[k]=receivedData[i];
				k++;
			}
			String keyInHM = new String(keyForHM);

			//Check if String matches any Key of HashMap, if yes then it is already cached.
			if(proxy.containsKey(keyInHM)){
				System.out.println("Value is cached, sending cached value\n");

				//Re-attach the query Id and send the response to terminal.
				byte[] toTermCachedVal = new byte[ARRAY_SIZE];
				toTermCachedVal[0] = receivedData[0];
				toTermCachedVal[1] = receivedData[1];
				int v=2;
				for(int i=0; i<proxy.get(keyInHM).length; i++){
					toTermCachedVal[v] = proxy.get(keyInHM)[i];
					v++;
				}
				DatagramPacket packCache = new DatagramPacket(toTermCachedVal, toTermCachedVal.length, termIP, termPort);
				serverSocket.send(packCache);
			}
			else{
				//Else our proxy server will now act as a client. Send request to Nameserver.
				DatagramSocket toNS = new DatagramSocket();
				toNS.setSoTimeout(10000);
				byte[] response = new byte[ARRAY_SIZE];
				DatagramPacket toNSResponse = new DatagramPacket(response, response.length);

				//Packet received from Terminal is sent to Local DNS Server.
				InetAddress nameServerIP = InetAddress.getByName(NS_IP);
				DatagramPacket resPack = new DatagramPacket(receivedData, receivedData.length, nameServerIP , STD_NS_PORT);
				toNS.send(resPack);

				/*
				 * Received Response is stored in a new byte array and it is put in
				 * the existing Hashmap. The key of the Hashmap will be the created String
				 * withut the Query ID as query ID can vary with each query. While storing
				 * the response in HashMap, remove the query ID too, so it can be appended
				 * to the query ID of the particular query
				 * */

				try{
					toNS.receive(toNSResponse);byte[] valForHM = new byte[HASH_SIZE];
					k=0;
					for(int i=2; i<response.length; i++){
						valForHM[k] = response[i];
						k++;
					}

					//Store only CACHE_SIZE recent entries.
					if(entries>=CACHE_SIZE){
						proxy.remove(recent.get(entries%CACHE_SIZE+1));
					}
					proxy.put(keyInHM, valForHM);
					recent.put(entries%CACHE_SIZE+1, keyInHM);
					entries++;

					//After caching send the response to terminal, IP and Port are stored initially
					DatagramPacket toTerminal = new DatagramPacket(response, response.length, termIP, termPort);
					serverSocket.send(toTerminal);
				}
				catch(IOException e){
					//System.out.println("Timeout");
				}
			}
		}
	}
}
