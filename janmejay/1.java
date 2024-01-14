import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

class Account {
    private double balance;
    private final String accountNumber;

    public Account(String accountNumber, double initialBalance) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
    }

    public synchronized void deposit(double amount) {
        balance += amount;
        logTransaction("Deposit", amount);
    }

    public synchronized void withdraw(double amount) {
        if (amount <= balance) {
            balance -= amount;
            logTransaction("Withdrawal", amount);
        } else {
            System.out.println("Insufficient funds");
        }
    }

    public synchronized double getBalance() {
        return balance;
    }

    private void logTransaction(String transactionType, double amount) {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String timestamp = dateFormat.format(new Date());
        System.out.println(String.format("[%s] %s of %.2f from account %s", timestamp, transactionType, amount, accountNumber));
    }
}

class Bank {
    private final Map<String, Account> accounts = new HashMap<>();

    public void createAccount(String accountNumber, double initialBalance) {
        Account account = new Account(accountNumber, initialBalance);
        accounts.put(accountNumber, account);
    }

    public Account getAccount(String accountNumber) {
        return accounts.get(accountNumber);
    }
}

class BankGUI extends JFrame {
    private final Bank bank;

    private final JTextField accountNumberField;
    private final JTextField amountField;
    private final JTextArea logArea;

    public BankGUI(Bank bank) {
        this.bank = bank;

        // Initialize components
        accountNumberField = new JTextField(10);
        amountField = new JTextField(10);
        logArea = new JTextArea(10, 30);

        JButton depositButton = new JButton("Deposit");
        JButton withdrawButton = new JButton("Withdraw");
        JButton balanceButton = new JButton("Check Balance");

        // Set layout
        setLayout(new FlowLayout());

        // Add components to the frame
        add(new JLabel("Account Number: "));
        add(accountNumberField);
        add(new JLabel("Amount: "));
        add(amountField);
        add(depositButton);
        add(withdrawButton);
        add(balanceButton);
        add(new JScrollPane(logArea));

        // Set action listeners
        depositButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                performTransaction("Deposit");
            }
        });

        withdrawButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                performTransaction("Withdraw");
            }
        });

        balanceButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                checkBalance();
            }
        });

        // Set frame properties
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(400, 300);
        setVisible(true);
    }

    private void performTransaction(String transactionType) {
        String accountNumber = accountNumberField.getText();
        double amount = Double.parseDouble(amountField.getText());

        Account account = bank.getAccount(accountNumber);

        if (account != null) {
            if (transactionType.equals("Deposit")) {
                account.deposit(amount);
            } else if (transactionType.equals("Withdraw")) {
                account.withdraw(amount);
            }
        } else {
            System.out.println("Account not found");
        }

        updateLog();
    }

    private void checkBalance() {
        String accountNumber = accountNumberField.getText();
        Account account = bank.getAccount(accountNumber);

        if (account != null) {
            logArea.append(String.format("Balance of account %s: %.2f\n", accountNumber, account.getBalance()));
        } else {
            System.out.println("Account not found");
        }
    }

    private void updateLog() {
        logArea.setText(""); // Clear the log area
    }
}

public class MultiThreadBankingSystem {
    public static void main(String[] args) {
        Bank bank = new Bank();
        bank.createAccount("12345", 1000);
        bank.createAccount("67890", 500);

        SwingUtilities.invokeLater(() -> new BankGUI(bank));
    }
}