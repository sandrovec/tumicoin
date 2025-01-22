class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 2
        self.user_balances = {}  # Diccionario para manejar balances de usuarios

    def create_genesis_block(self):
        return Block(0, "0", [], time.time())

    def get_latest_block(self):
        return self.chain[-1]

    def create_account(self, email):
        if email in self.user_balances:
            raise ValueError("La cuenta ya existe.")
        self.user_balances[email] = 0

    def get_balance(self, email):
        if email not in self.user_balances:
            raise ValueError("La cuenta no existe.")
        return self.user_balances[email]

    def add_transaction(self, sender, recipient, amount):
        if sender not in self.user_balances or recipient not in self.user_balances:
            raise ValueError("Cuentas involucradas no existen.")
        if self.user_balances[sender] < amount:
            raise ValueError("Saldo insuficiente.")

        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def mine_pending_transactions(self):
        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            transactions=self.pending_transactions
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

        # Actualizar balances de usuarios
        for tx in self.pending_transactions:
            sender, recipient, amount = tx["sender"], tx["recipient"], tx["amount"]
            self.user_balances[sender] -= amount
            self.user_balances[recipient] += amount

        self.pending_transactions = []

    def get_user_transactions(self, email):
        transactions = []
        for block in self.chain:
            for tx in block.transactions:
                if tx["sender"] == email or tx["recipient"] == email:
                    transactions.append(tx)
        return transactions
