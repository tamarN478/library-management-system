class Library:
    def __init__(self):
        self.books={}
        self.membership=[]
        self.prices = {}
        self.bought_books={}
        self.borrowed_books={}
        self.reserved_books={}
        self.fines={}

    def add_book(self, book, quantity=1):
        if book in self.books:
            self.books[book] += quantity
        else:
            self.books[book] = quantity
        print(f"Added {quantity} copy/copies of '{book}'. Total in stock: {self.books[book]}")

    def remove_book(self, book, quantity=1):
        if book not in self.books or self.books[book] <= 0:
            print(f"Cannot remove '{book}'—it is not in the library.")
            return
        if quantity >= self.books[book]:
            del self.books[book]
            print(f"Removed all copies of '{book}' from the library.")
        else:
            self.books[book] -= quantity
            print(f"Removed {quantity} copy/copies of '{book}'. Remaining stock: {self.books[book]}")  

    def add_member(self, member):
        member = member.strip().title()
        if member not in self.membership:
            self.membership.append(member)
        else:
            print(f"{member} is already a member.")

    def cancel_membership(self, member):
        if member in self.membership:
            self.membership.remove(member)
        else:
            print(f"{member} is not found.")

    def set_book_price(self, book, price):
        self.prices[book] = price        

    def buy_book(self, member, book):
        member = member.strip().title()
        if book not in self.books or self.books[book] <= 0:
            print(f"Sorry, '{book}' is currently out of stock.")
            return
        
        if book not in self.prices:
            print(f"{book} is not available for purchase.")
            return
        base_price= self.prices[book]

        if member in self.membership: 
            final_price= base_price * 0.75
        else:
            final_price=base_price

        self.books[book] -= 1    

        self.bought_books[book] = {
            "buyer": member,
            "price_paid": final_price}

        print(f"{member} bought '{book}' for ${final_price:.2f}")
        return final_price    

    def borrow_book(self, member, book):
        if book not in self.books or self.books[book] <= 0:
            print(f"Sorry, '{book}' is not available to borrow.")
            return

        self.books[book] -= 1

        if book not in self.borrowed_books:
            self.borrowed_books[book] = []
        self.borrowed_books[book].append(member)

        print(f"{member} borrowed '{book}'. Remaining available copies: {self.books[book]}")
            

    def return_book(self, member, book):
        if book in self.borrowed_books and member in self.borrowed_books[book]:
            self.borrowed_books[book].remove(member)
            
            self.books[book] = self.books.get(book, 0) + 1
            print(f"{member} returned '{book}'. Stock increased to: {self.books[book]}")
        else:
            print(f"No record of {member} borrowing '{book}'.")
           

    def reserve_book(self, member, book):
        if book not in self.books:
            print(f"Sorry, '{book}' does not exist in our library catalog.")
            return
        if book in self.reserved_books and member in self.reserved_books[book]:
            print(f"{member} has already reserved '{book}'.")
            return
        if book not in self.reserved_books:
            self.reserved_books[book] = []
        self.reserved_books[book].append(member)
        print(f"{member} successfully reserved '{book}'.")

    def cancel_reservation(self, member, book):
        if book in self.reserved_books and member in self.reserved_books[book]:
            self.reserved_books[book].remove(member)
            print(f"{member} canceled reservation for '{book}'.")
        else:
            print(f"No reservation found for {member} on '{book}'.")

    def calculate_fine(self, member, book, days_late):
        if days_late <= 0:
            print("was returned on time.")
            return 0
        fine_per_day = 1.0
        total_fine= fine_per_day * days_late
        if member in self.fines:
            self.fines[member] += total_fine
        else:
            self.fines[member] = total_fine
            print(f"{member} has a fine of ${total_fine:.2f} for returning '{book}' {days_late} days late.")
            
        
my_library = Library()
#setup
my_library.add_book("1984", quantity=12)
my_library.add_book("Little Women", quantity=10)
my_library.add_book("A Song of Ice and Fire", quantity=15)
my_library.add_book("Anna Karenina", quantity=10)
my_library.add_book("Pride and Prejudice", quantity=5)
my_library.add_book("Hamlet", quantity=14)

my_library.set_book_price("1984", 20.00)
my_library.set_book_price("Little Women", 15.00)
my_library.set_book_price("A Song of Ice and Fire", 25.00)
my_library.set_book_price("Anna Karenina", 18.00)
my_library.set_book_price("Pride and Prejudice", 22.00)
my_library.set_book_price("Hamlet", 16.00)

my_library.add_member("Lola")
my_library.add_member("Bob")
my_library.add_member("Mary")
my_library.add_member("Mike")
my_library.add_member("Hannah")

#transactions
my_library.buy_book("Lola", "1984")    
my_library.buy_book("Mary", "A Song of Ice and Fire") 
my_library.buy_book("Charlie", "Anna Karenina") 
my_library.buy_book("Alison", "Pride and Prejudice")

my_library.borrow_book("Bob", "A Song of Ice and Fire")
my_library.borrow_book("Nina", "Pride and Prejudice")
my_library.borrow_book("Emily", "1984")
my_library.borrow_book("Arya", "Little Women")

my_library.reserve_book("Spencer", "Hamlet") 
my_library.reserve_book("Mike", "Little Women")   
my_library.reserve_book("Hannah", "Hamlet") 

my_library.return_book("Bob", "A Song of Ice and Fire")
my_library.return_book("Nina", "Pride and Prejudice")
my_library.return_book("Emily", "1984")

my_library.calculate_fine("Arya", "Little Women", 3) 

print("\n" + "="*40 + "\n")

#display

print('books & prices')
for book, stock in my_library.books.items():
    price = my_library.prices.get(book, "N/A")
    print(f"  - {book}: {stock} in stock (${price:.2f})")

print('\nmembers')
for member in my_library.membership:
    print(f"  - {member}")

print('\npurchased books') 
if my_library.bought_books:
    for book, info in my_library.bought_books.items():
        print(f"  - '{book}' bought by {info['buyer']} for ${info['price_paid']:.2f}")
else:
    print("  - No purchased books recorded.")

print('\nborrowed books')
# Displays only books that are currently borrowed
active_borrows = False
for book, borrowers in my_library.borrowed_books.items():
    if borrowers:
        active_borrows = True
        print(f"  - '{book}': borrowed by {', '.join(borrowers)}")
if not active_borrows:
    print("  - No active borrows.")

print('\nreserved books')
for book, reservables in my_library.reserved_books.items():
    if reservables:
        print(f"  - '{book}': reserved by {', '.join(reservables)}")

print('\nfines')
for member, amount in my_library.fines.items():
    print(f"  - {member}: ${amount:.2f}")

