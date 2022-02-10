


# TokenClaimPortal
<h2>Author</h2>
<ul>
<li>Nicolas Fernandez Sanz</li>
</ul>
<h2>Important</h2>
This is a <strong>sample repository </strong>, images and logos were removed. As well as some parts of the code that could compromise the security of the final system. I do not recommend, under any point of view, operating this system for other purposes.

<h2>Description</h2>
Web portal designed to authenticate users and allow them to withdraw a certain amount of tokens on a regular basis. This is a <strong>adaptation of the final project for demonstration purposes</strong>.This application aims to be secure since its main objective is the distribution of a token with real monetary value. Almost all procedures are performed server-side, on <strong>servers with high security standards</strong>.

<h3>Authentication</h3>
<ul>
<li> Users login using their <a href="https://academy.binance.com/en/glossary/blockchain?utm_campaign=googleadsxacademy&utm_source=googleads&utm_medium=cpc&gclid=Cj0KCQiAjJOQBhCkARIsAEKMtO1D6x_PC4IJ5wxPGz_J7mE9eNRv_a2CmkNSom43X6c9MlEY8sanmTQaAqpREALw_wcB"> Binance Smart Chain wallet </a>, this allows the credentials to be highly secure and backed by the blockchain. No one without access to your crypto wallet will be able to log in to the portal for you. You can connect any <a href="https://chrome.google.com/webstore/detail/metamask/nkbihfbeogaeaoehlefnkodbefgpgknn"> Metamask wallet </a> or any wallet compatible with <a href="https://walletconnect.com/">WalletConnect</a></li>
<li> <a href="https://discord.com/"> Discord </a> OAUTH2, this is an optional step, but allows the staff members to easily communicate with you. We automatically link your discord account with your wallet.</li>
<li><a href="https://web.telegram.org/">Telegram</a> OAUTH2, same as discord.</li>
</ul>

<h3>User Portal</h3>

Based on the information stored in a MySQL database and the exploration of the Blockchain, the user portal will display a lot of info associated to your account. You will be able to see the progress of the token distribution in real-time, contact with support, see the status of different in-game stadistics and much more.


<h3>Token Distribution</h3>

In this example, I used a wallet to wallet transaction. This a cheap alternative if you have only a few transactions per day.. Anyway if you are planing to have many "Claim transactions" I highly reccommend the implementation of a SmartContract. The production version of this app has a SmartContract.
The system is designed to validate each transaction before executing on two mirrored databases, this prevents any attempt to hack a database from taking control of the system.


<h2>Installation</h2>
The system could be run in a Linux Virtual Machine using nginx and gunicorn. All the dependencys are detailed in the `requirements.txt` file. 
If you are planning to have a high demand I recommend using a balancer, or a kubernets pod.
