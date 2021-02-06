from app import db
from models import Book

db.drop_all()
db.create_all()

hp_ss = Book.add_book(
    "Harry Potter and the Sorcerer’s Stone",
    """Harry Potter's life is miserable. His parents are dead and he's stuck with his heartless relatives,
    who force him to live in a tiny closet under the stairs. But his fortune changes when he receives a 
    letter that tells him the truth about himself: he's a wizard. A mysterious visitor rescues him from 
    his relatives and takes him to his new home, Hogwarts School of Witchcraft and Wizardry.

    After a lifetime of bottling up his magical powers, Harry finally feels like a normal kid. But even 
    within the Wizarding community, he is special. He is the boy who lived: the only person to have ever 
    survived a killing curse inflicted by the evil Lord Voldemort, who launched a brutal takeover of the 
    Wizarding world, only to vanish after failing to kill Harry.

    Though Harry's first year at Hogwarts is the best of his life, not everything is perfect. There is a 
    dangerous secret object hidden within the castle walls, and Harry believes it's his responsibility to 
    prevent it from falling into evil hands. But doing so will bring him into contact with forces more 
    terrifying than he ever could have imagined.

    Full of sympathetic characters, wildly imaginative situations, and countless exciting details, the first 
    installment in the series assembles an unforgettable magical world and sets the stage for many high-stakes 
    adventures to come.""",
    "J.K. Rowling",
    "Fantasy",
    1997,
    "https://m.media-amazon.com/images/I/413lxIe20jL.jpg"
)
hp_cs = Book.add_book(
    "Harry Potter and the Chamber of Secrets",
    """Ever since Harry Potter had come home for the summer, the Dursleys had been so mean and hideous that all 
    Harry wanted was to get back to the Hogwarts School for Witchcraft and Wizardry. But just as he’s packing his 
    bags, Harry receives a warning from a strange impish creature who says that if Harry returns to Hogwarts, 
    disaster will strike.

    And strike it does. For in Harry’s second year at Hogwarts, fresh torments and horrors arise, including an 
    outrageously stuck-up new professor and a spirit who haunts the girls’ bathroom. But then the real trouble 
    begins – someone is turning Hogwarts students to stone. Could it be Draco Malfoy, a more poisonous rival than 
    ever? Could it possible be Hagrid, whose mysterious past is finally told? Or could it be the one everyone at 
    Hogwarts most suspects… Harry Potter himself! """,
    "J.K. Rowling",
    "Fantasy",
    1998,
    "https://images-na.ssl-images-amazon.com/images/I/51TA3VfN8RL._SX342_SY445_QL70_ML2_.jpg"
)
hp_pa = Book.add_book(
    "Harry Potter and the Prisoner of Azkaban",
    """For twelve long years, the dread fortress of Azkaban held an infamous prisoner named Sirius Black. Convicted
    of killing thirteen people with a single curse, he was said to be the heir apparent to the Dark Lord, Voldemort.

    Now he has escaped, leaving only two clues as to where he might be headed: Harry Potter's defeat of You-Know-Who 
    was Black's downfall as well. And the Azkaban guards heard Black muttering in his sleep, "He's at Hogwarts . . . 
    he's at Hogwarts."

    Harry Potter isn't safe, not even within the walls of his magical school, surrounded by his friends. Because on 
    top of it all, there may well be a traitor in their midst. """,
    "J.K. Rowling",
    "Fantasy",
    1999,
    "https://m.media-amazon.com/images/I/51Dfqo6jR5L.jpg"
)
hp_gf = Book.add_book(
    "Harry Potter and the Goblet of Fire",
    """Harry Potter is midway through his training as a wizard and his coming of age. Harry wants to get away from the 
    pernicious Dursleys and go to the International Quidditch Cup with Hermione, Ron, and the Weasleys. He wants to 
    dream about Cho Chang, his crush (and maybe do more than dream). He wants to find out about the mysterious event 
    that's supposed to take place at Hogwarts this year, an event involving two other rival schools of magic, and a 
    competition that hasn't happened for hundreds of years. He wants to be a normal, fourteen-year-old wizard. But 
    unfortunately for Harry Potter, he's not normal - even by wizarding standards.

    And in his case, different can be deadly. """,
    "J.K. Rowling",
    "Fantasy",
    2000,
    "https://m.media-amazon.com/images/I/51Vjb2qJwzL.jpg"
)
hp_op = Book.add_book(
    "Harry Potter and the Order of the Phoenix",
    """Harry has a lot on his mind for this, his fifth year at Hogwarts: a Defense Against the Dark Arts teacher with a 
    personality like poisoned honey; a big surprise on the Gryffindor Quidditch team; and the looming terror of the 
    Ordinary Wizarding Level exams. But all these things pale next to the growing threat of He-Who-Must-Not-Be-Named - a 
    threat that neither the magical government nor the authorities at Hogwarts can stop.

    As the grasp of darkness tightens, Harry must discover the true depth and strength of his friends, the importance of 
    boundless loyalty, and the shocking price of unbearable sacrifice.

    His fate depends on them all. """,
    "J.K. Rowling",
    "Fantasy",
    2003,
    "https://m.media-amazon.com/images/I/51-SI2+aQ2L.jpg"
)
hp_hbp = Book.add_book(
    "Harry Potter and the Half-Blood Prince",
    """The war against Voldemort is not going well; even Muggle governments are noticing. Ron scans the obituary pages of 
    the Daily Prophet, looking for familiar names. Dumbledore is absent from Hogwarts for long stretches of time, and the Order 
    of the Phoenix has already suffered losses.

    And yet . . .

    As in all wars, life goes on. The Weasley twins expand their business. Sixth-year students learn to Apparate - and lose a few 
    eyebrows in the process. Teenagers flirt and fight and fall in love. Classes are never straightforward, through Harry receives 
    some extraordinary help from the mysterious Half-Blood Prince.

    So it's the home front that takes center stage in the multilayered sixth installment of the story of Harry Potter. Here at 
    Hogwarts, Harry will search for the full and complete story of the boy who became Lord Voldemort - and thereby find what may be 
    his only vulnerability. """,
    "J.K. Rowling",
    "Fantasy",
    2005,
    "https://m.media-amazon.com/images/I/51myHyjJsyL.jpg"
)
hp_dh = Book.add_book(
    "Harry Potter and the Deathly Hallows",
    """Harry Potter is leaving Privet Drive for the last time. But as he climbs into the sidecar of Hagrid’s motorbike and they take 
    to the skies, he knows Lord Voldemort and the Death Eaters will not be far behind.

    The protective charm that has kept him safe until now is broken. But the Dark Lord is breathing fear into everything he loves. 
    And he knows he can’t keep hiding.

    To stop Voldemort, Harry knows he must find the remaining Horcruxes and destroy them.

    He will have to face his enemy in one final battle.""",
    "J.K. Rowling",
    "Fantasy",
    2007,
    "https://m.media-amazon.com/images/I/511DhzIj4cL.jpg"
)

db.session.add_all([hp_ss, hp_cs, hp_pa, hp_gf, hp_op, hp_hbp, hp_dh])
db.session.commit()