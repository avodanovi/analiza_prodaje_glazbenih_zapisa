import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from dateutil.relativedelta import relativedelta

#ispis cijelog dataframe-a
def print_full(x):
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    print(x)

#pronalazi najboljeg prodavaca u odredeđenom razdoblju
def best_seller(start,stop):

    data = []
    for i, employee in dfEmployees.iterrows():
        quantity = 0
        soldPrice = 0
        for ind, costumer in dfCostumers.iterrows():
            if employee['EmployeeId'] == costumer["SupportRepId"]:
                for inde, invoice in dfInvoice.iterrows():
                    if stop <= pd.to_datetime(invoice['InvoiceDate']) <= start:
                        if costumer['CustomerId'] == invoice['CustomerId']:
                            for index, item in dfInvocieItems.iterrows():
                                if invoice['InvoiceId'] == item['InvoiceId']:
                                    quantity += item['Quantity']
                                    soldPrice += item['Quantity'] * item['UnitPrice']
        data.append([employee['FirstName'], employee['LastName'], quantity, soldPrice])


    dfBestSeller = pd.DataFrame(data, columns=['Name', 'Lastname', 'Quantity', 'TotalSold'],index=None).sort_values(['TotalSold'],ascending=False)

    print('\nPopis top 3 prodavaca u razdoblju od %s do %s :'%(stop.date(),start.date()))
    print(dfBestSeller.head(3))

    bestSeller = dfBestSeller.iloc[0]

    print('Najbolji prodavac u razdoblju od %s do %s je %s %s. Prodao je %.2f proizvoda ukupne vrijednosti %.3f .'% (stop.date(),start.date(),bestSeller['Name'],bestSeller['Lastname'],bestSeller['Quantity'],bestSeller['TotalSold']))

    monthData={}
    for i in data:
        key=i[0]+' '+i[1]
        monthData[key]=i[2]
    return monthData

#pronalazi grad s najvise prodaja u određenom razdoblju
def best_selling_cities(start,stop):
    cityValue = {}
    cityQuantity = {}
    for i, costumer in dfCostumers.iterrows():
        cityValue[str(costumer['City']) + ',' + str(costumer['Country'])] = 0
        cityQuantity[str(costumer['City']) + ',' + str(costumer['Country'])] = 0

    for i, employee in dfEmployees.iterrows():
        for ind, costumer in dfCostumers.iterrows():
            if employee['EmployeeId'] == costumer["SupportRepId"]:
                for i, invoice in dfInvoice.iterrows():
                    if stop <= pd.to_datetime(invoice['InvoiceDate']) <= start:
                        if costumer['CustomerId'] == invoice['CustomerId']:
                            for ind, invoiceLine in dfInvocieItems.iterrows():
                                if invoice['InvoiceId'] == invoiceLine["InvoiceId"]:
                                    key = str(costumer['City']) + ',' + str(costumer['Country'])
                                    cityValue[key] += invoiceLine['UnitPrice'] * \
                                                          invoiceLine['Quantity']
                                    cityQuantity[key] += invoiceLine['Quantity']

    dfCityValue = pd.Series(cityValue).sort_values(ascending=False)
    dfCityQuantity = pd.Series(cityQuantity).sort_values(ascending=False)

    print('\nPopis prvih deset gradova prema ukupnoj vrijednosti kupnje u razdoblju od %s do %s :'%(stop.date(),start.date()))
    print(dfCityValue.head(10))
    print('\n\n')
    print('\nPopis prvih deset gradova prema kolicini kupljenih proizvodau razdoblju od %s do %s :'%(stop.date(),start.date()))
    print(dfCityQuantity.head(10))

#pronalazi muziku koja se najbolje prodavala u određenom razdoblju
def best_selling_music(start,stop):
    best_selling_songs = {}
    best_selling_albums = {}
    best_selling_artist = {}
    best_selling_genre = {}

    for i, song in dfTracks.iterrows():
        # best_selling_songs[song['Name']]=0
        best_selling_songs[song['Name']] = 0
    for i, album in dfAlbums.iterrows():
        best_selling_albums[album['Title']] = 0
    for i, artist in dfArtists.iterrows():
        best_selling_artist[artist['Name']] = 0
    for i, genre in dfGenre.iterrows():
        best_selling_genre[genre['Name']] = 0

    for i, invoice in dfInvoice.iterrows():
        if stop <= pd.to_datetime(invoice['InvoiceDate']) <= start:
            for ind, item in dfInvocieItems.iterrows():
                if invoice['InvoiceId'] == item['InvoiceId']:
                    for inde, track in dfTracks.iterrows():
                        if item['TrackId'] == track['TrackId']:
                            best_selling_songs[track['Name']] += 1
                            for index, genre in dfGenre.iterrows():
                                if track['GenreId'] == genre['GenreId']:
                                    best_selling_genre[genre['Name']] += 1
                            for indexx, album in dfAlbums.iterrows():
                                if track['AlbumId'] == album['AlbumId']:
                                    best_selling_albums[album['Title']] += 1
                                    for indexxx, artist in dfArtists.iterrows():
                                        if album['ArtistId'] == artist['ArtistId']:
                                            best_selling_artist[artist['Name']] += 1

    dfBest_selling_songs = pd.Series(best_selling_songs).sort_values(ascending=False)
    dfBest_selling_albums = pd.Series(best_selling_albums).sort_values(ascending=False)
    dfBest_selling_artist = pd.Series(best_selling_artist).sort_values(ascending=False)
    dfBest_selling_genre = pd.Series(best_selling_genre).sort_values(ascending=False)

    print('\nBest selling songs from %s to %s: '%(start,stop))
    print(dfBest_selling_songs.head())
    print('\nBest selling artists from %s to %s: '%(start,stop))
    print(dfBest_selling_artist.head())
    print('\nBest selling albums from %s to %s: '%(start,stop))
    print(dfBest_selling_albums.head())
    print('\nBest selling genres from %s to %s: '%(start,stop))
    print(dfBest_selling_genre.head())

#pronalazi najprodavanije žanrove prodavaca
def seller_best_genres():
    employees = []
    genresList = []
    for i, employee in dfEmployees.iterrows():
        employees.append(str(employee['FirstName'] + ' ' + employee['LastName']))
        genres = {}
        for ind, costumer in dfCostumers.iterrows():
            if employee['EmployeeId'] == costumer["SupportRepId"]:
                for inde, invoice in dfInvoice.iterrows():
                    if costumer['CustomerId'] == invoice['CustomerId']:
                        for index, item in dfInvocieItems.iterrows():
                            if invoice['InvoiceId'] == item['InvoiceId']:
                                for inde, track in dfTracks.iterrows():
                                    if item['TrackId'] == track['TrackId']:
                                        for index, genre in dfGenre.iterrows():
                                            if track['GenreId'] == genre['GenreId']:
                                                if genre['Name'] in genres.keys():
                                                    genres[genre['Name']] += 1
                                                else:
                                                    genres[genre['Name']] = 1

        genresList.append(genres)

    df = pd.DataFrame(genresList, index=employees)
    print_full(df)

#pronalazi koji su zanrovi popularni u pojedinom gradu u određenom razdoblju
def best_cities_per_genre(start,stop,sortby='Rock'):
    cities = []
    genresList = []


    for ind, costumer in dfCostumers.iterrows():
        cityState = costumer['City'] + ',' + costumer['Country']
        if cityState not in cities:
            cities.append(cityState)


    for city in cities:
        genres={}
        for ind, costumer in dfCostumers.iterrows():
            city_State = costumer['City'] + ',' + costumer['Country']
            if city ==city_State:
                for inde, invoice in dfInvoice.iterrows():
                    if stop <= pd.to_datetime(invoice['InvoiceDate']) <= start:
                        if costumer['CustomerId'] == invoice['CustomerId']:
                            for index, item in dfInvocieItems.iterrows():
                                if invoice['InvoiceId'] == item['InvoiceId']:
                                    for inde, track in dfTracks.iterrows():
                                        if item['TrackId'] == track['TrackId']:
                                            for index, genre in dfGenre.iterrows():
                                                if track['GenreId'] == genre['GenreId']:
                                                    if genre['Name'] in genres.keys():
                                                        genres[genre['Name']] += 1
                                                    else:
                                                        genres[genre['Name']] = 1

        genresList.append(genres)


    dfCitiesPerGenre = pd.DataFrame(genresList, index=cities).sort_values([sortby],ascending=False)
    print_full(dfCitiesPerGenre)

#pronalazi najprodavanije zanrove u odredenom razdoblju
def best_selling_genres(start,stop):
    genres = {}
    for inde, invoice in dfInvoice.iterrows():
        if stop <= pd.to_datetime(invoice['InvoiceDate']) <= start:
            for index, item in dfInvocieItems.iterrows():
                if invoice['InvoiceId'] == item['InvoiceId']:
                    for inde, track in dfTracks.iterrows():
                        if item['TrackId'] == track['TrackId']:
                            for index, genre in dfGenre.iterrows():
                                if track['GenreId'] == genre['GenreId']:
                                    if genre['Name'] in genres.keys():
                                        genres[genre['Name']] += 1
                                    else:
                                        genres[genre['Name']] = 1



    dfSellGenres = pd.Series(genres).sort_values(ascending=False)
    print('Najbolje prodavani zanrovi u razdoblju od %s do %s'%(stop.date(),start.date()))
    print_full(dfSellGenres)
    return genres

#Funkcija ispisuje prodajne statistike svkog prodavaca u razlicitim vremenskim razdobljima,
#crta garfove prodjae po mjesecima u zadnje 4 godine
def best_seller_time():
    #za koju godinu zelimo pregled(0-zadnju, -1 predzadnju, ...)
    year = 0

    # najbolji prodavac u zadnjem tromjesecju
    data=best_seller(startOfDataset + relativedelta(years=year), startOfDataset + relativedelta(months=(- 3),years=year ))
    # najbolji prodavac u rzdoblju od 3. do 6. mjeseci prije kraja godine
    data=best_seller(startOfDataset + relativedelta(months=( - 3),years=year), startOfDataset + relativedelta(months=(-6),years=year ))
    # najbolji prodavac u razdoblju od 6. do 9. mjeseci prije prije kraja godine
    data=best_seller(startOfDataset + relativedelta(months=(- 6),years=year), startOfDataset + relativedelta(months=(- 9),years=year ))
    # najbolji prodavac u razdoblju od 9.mjeseca do godine dana prije kraja godine
    data=best_seller(startOfDataset + relativedelta(months=(- 9),years=year), startOfDataset + relativedelta(months=(-12),years=year ))
    #najbolji prodavac u  godinu dana
    data=best_seller(startOfDataset, startOfDataset + relativedelta(months=0 - 12,years=year))

    months= ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    for i in range(0,4):
        soldList = []
        for j in range(11,-1,-1):
            monthData=best_seller(startOfDataset + relativedelta(months=(-j),years=(-i)),startOfDataset + relativedelta(months=(-j-1),years=(-i)))
            soldList.append(monthData)
        dfMonthSale = pd.DataFrame(soldList, index=months)
        print(dfMonthSale)

        namePlt= str((startOfDataset + relativedelta(years=(-i))).year) +'. godina'
        savePlt = 'Sales_per_month_year_'+str((startOfDataset + relativedelta(years=(-i))).year) +'.jpg'
        fig = plt.figure()
        fig.set_figwidth(12)
        fig.set_figheight(6)
        plt.plot(dfMonthSale)
        plt.legend(['Jane Peacock','Margaret Park','Steve Johnson'])
        fig.suptitle(namePlt)
        plt.ylabel('Num. of sales')
        fig.savefig(savePlt)
        plt.show()

#iscrtava graf najprodavnijih zanrova zadnjih godinu dana
def best_selling_genres_last_year():
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    soldList = []
    for j in range(11, -1, -1):
        monthData = best_selling_genres(startOfDataset + relativedelta(months=(-j)),
                                        startOfDataset + relativedelta(months=(-j - 1)))

        soldList.append(monthData)
    dfMonthSale = pd.DataFrame(soldList, index=months)

    dfMonthSale.rank(ascending=False).plot(kind='bar', figsize=(18, 12)).legend(loc='best')
    plt.savefig('genres_per_month_last_year.png')
    plt.show()


#ucitavanje podataka iz baza u dataframe-ove
con = sqlite3.connect("data/tracksalesdb.db")
dfEmployees = pd.read_sql_query("SELECT EmployeeId,FirstName,LastName, HireDate FROM employees WHERE EmployeeId IN (SELECT SupportRepId FROM customers) ", con)
dfCostumers = pd.read_sql_query("SELECT SupportRepId, CustomerId,City,Country FROM customers ",con)
dfInvoice = pd.read_sql_query("SElECT CustomerId,InvoiceId,InvoiceDate,BillingCity,BillingCountry FROM invoices",con)
dfInvocieItems = pd.read_sql_query("SElECT InvoiceId,UnitPrice,Quantity,TrackId FROM invoice_items",con)
dfTracks =pd.read_sql_query("SElECT * FROM tracks",con)
dfMediaType =pd.read_sql_query("SElECT * FROM media_types",con)
dfGenre =pd.read_sql_query("SElECT * FROM genres",con)
dfPlaylistTrack =pd.read_sql_query("SElECT * FROM playlist_track",con)
dfPlaylist=pd.read_sql_query("SElECT * FROM playlists",con)
dfArtists = pd.read_sql_query("SElECT * FROM artists",con)
dfAlbums = pd.read_sql_query("SElECT * FROM albums",con)

#datum prve/zadnje prodaje u bazi
startOfDataset=pd.to_datetime(dfInvoice['InvoiceDate']).max()
stopOfDataset = pd.to_datetime(dfInvoice['InvoiceDate']).min()



#ispisuje podatke o najboljem prodavacu u razlicitim vremenskim razdobljima
#crta graf uspjesnosti prodavaca za prosle 4 godine
best_seller_time()

#Najbolje prodavana pjesma u zadnja 3 mjeseca
best_selling_music(startOfDataset,startOfDataset + relativedelta(months=(-3 )))

#gradovi s najboljom prodajom u zadnjih godinu dana
best_selling_cities(startOfDataset,startOfDataset + relativedelta(months=(-12 )))

#Najprodavaniji zanrovi po gradu u zadnjih godinu dana
best_cities_per_genre(startOfDataset,startOfDataset + relativedelta(months=(-12 )))

#najprodavaniji zanrovi po prodavacu
seller_best_genres()

#najprodavaniji zanrovi u posljednjih godinu dana
best_selling_genres(startOfDataset,startOfDataset + relativedelta(months=(-12 )))

#crta graf prodaje zanrova po mjesecima za proslu godinu
best_selling_genres_last_year()

con.close()