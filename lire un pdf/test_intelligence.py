#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'intelligence artificielle améliorée pour l'extraction des dates de livraison
"""

import json
import re
from datetime import datetime
import dateutil.parser

# Simulation de la fonction d'extraction intelligente
def extract_delivery_date_intelligent(text):
    """
    Fonction intelligente qui analyse le texte pour extraire les dates de livraison
    dans tous les formats possibles, y compris les phrases contextuelles complexes.
    """
    if not text:
        return None
    
    text_lower = text.lower()
    
    # Patterns pour détecter les phrases de livraison
    delivery_patterns = [
        # Phrases négatives avec dates
        r"(?:ne sera pas|pas de|impossible de|ne pourra pas).*?livr[ée]*.*?(?:avant le|avant|le)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"(?:livraison|livr[ée]*).*?(?:reportée|repoussée|décalée).*?(?:au|le|pour le)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"(?:délai|retard).*?(?:livraison|livr[ée]*).*?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        
        # Phrases positives avec dates
        r"(?:livraison|livr[ée]*).*?(?:prévue|estimée|planifiée).*?(?:le|pour le|au)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"(?:disponible|prêt).*?(?:le|pour le|au)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"(?:commande|colis).*?(?:livr[ée]*|expédi[ée]*).*?(?:le|pour le|au)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        
        # Formats abrégés
        r"(?:livraison|livr[ée]*)\s+(?:le|pour le|au)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"(?:prévu|estimé|planifié).*?(?:pour le|le|au)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        
        # Phrases avec contexte temporel
        r"(?:dans|en|vers|autour de)\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"(?:fin|début|mi).*?(?:semaine|mois).*?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        
        # Formats avec mots-clés temporels
        r"(?:semaine|mois).*?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",
        r"(?:prochaine|suivante).*?(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})"
    ]
    
    # Chercher d'abord les patterns de livraison
    for pattern in delivery_patterns:
        matches = re.findall(pattern, text_lower, re.IGNORECASE)
        if matches:
            for match in matches:
                try:
                    # Nettoyer et parser la date
                    date_str = match.strip()
                    if '/' in date_str:
                        # Format français DD/MM/YYYY ou DD/MM/YY
                        parts = date_str.split('/')
                        if len(parts) == 3:
                            day, month, year = parts
                            if len(year) == 2:
                                year = '20' + year
                            parsed_date = datetime(int(year), int(month), int(day))
                            return parsed_date.strftime('%d/%m/%Y')
                    elif '-' in date_str:
                        # Format avec tirets
                        parts = date_str.split('-')
                        if len(parts) == 3:
                            day, month, year = parts
                            if len(year) == 2:
                                year = '20' + year
                            parsed_date = datetime(int(year), int(month), int(day))
                            return parsed_date.strftime('%d/%m/%Y')
                except:
                    continue
    
    # Si aucun pattern de livraison trouvé, chercher toutes les dates dans le texte
    date_patterns = [
        r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # Format DD/MM/YYYY ou DD/MM/YY
        r'(\d{1,2}\s+(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+\d{4})',  # Format français
        r'(\d{1,2}\s+(?:jan|fév|mar|avr|mai|jun|jul|aoû|sep|oct|nov|déc)\s+\d{4})',  # Format français abrégé
    ]
    
    all_dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                if '/' in match or '-' in match:
                    # Format numérique
                    date_str = match.replace('-', '/')
                    parts = date_str.split('/')
                    if len(parts) == 3:
                        day, month, year = parts
                        if len(year) == 2:
                            year = '20' + year
                        parsed_date = datetime(int(year), int(month), int(day))
                        all_dates.append((parsed_date, match))
                else:
                    # Format français
                    try:
                        parsed_date = dateutil.parser.parse(match, dayfirst=True, fuzzy=True)
                        all_dates.append((parsed_date, match))
                    except:
                        continue
            except:
                continue
    
    # Si on a trouvé des dates, retourner la plus récente (probablement la date de livraison)
    if all_dates:
        # Trier par date et prendre la plus récente
        all_dates.sort(key=lambda x: x[0])
        most_recent = all_dates[-1]
        
        # Vérifier si c'est une date future (probablement une date de livraison)
        if most_recent[0] > datetime.now():
            return most_recent[0].strftime('%d/%m/%Y')
        else:
            # Si pas de date future, retourner la plus récente trouvée
            return most_recent[0].strftime('%d/%m/%Y')
    
    return None

def test_extraction():
    """Test de l'extraction intelligente avec différents formats d'emails"""
    
    # Cas de test 1 : Phrase négative complexe
    test1 = """
    Bonjour,
    
    Concernant votre commande BSK2506CF0383, nous avons un problème de stock.
    La commande ne sera pas livrée avant le 12/10/25 comme prévu initialement.
    
    Cordialement,
    IMPRIMERIE AJDIR
    """
    
    # Cas de test 2 : Phrase positive avec contexte
    test2 = """
    Bonjour,
    
    Votre commande TAC ETAC60JDF est maintenant en cours de production.
    Livraison prévue pour le 15/10/2025.
    
    Cordialement,
    IMPRIMERIE AJDIR
    """
    
    # Cas de test 3 : Phrase informelle
    test3 = """
    Salut,
    
    Désolé mais on ne pourra pas livrer avant le 25/10.
    Il y a eu un retard dans la production.
    
    Cordialement
    """
    
    # Cas de test 4 : Phrase avec report
    test4 = """
    Bonjour,
    
    Suite à un problème technique, la livraison de votre commande est reportée au 20/10/2025.
    
    Cordialement
    """
    
    # Cas de test 5 : Format abrégé
    test5 = """
    Bonjour,
    
    Livraison le 30/10/2025.
    
    Cordialement
    """
    
    # Cas de test 6 : Phrase complexe avec contexte
    test6 = """
    Bonjour,
    
    Nous avons bien reçu votre commande. Cependant, en raison des délais de production,
    il ne sera pas possible de livrer avant le 18/10/25. Nous faisons de notre mieux
    pour respecter cette nouvelle échéance.
    
    Cordialement
    """
    
    # Cas de test 7 : Phrase avec format français
    test7 = """
    Bonjour,
    
    La commande sera disponible le 22 octobre 2025.
    
    Cordialement
    """
    
    # Cas de test 8 : Phrase très informelle
    test8 = """
    Salut,
    
    Impossible de livrer avant le 28/10. Désolé pour le contretemps.
    
    Cordialement
    """
    
    tests = [
        ("Test 1 - Phrase négative complexe", test1),
        ("Test 2 - Phrase positive avec contexte", test2),
        ("Test 3 - Phrase informelle", test3),
        ("Test 4 - Phrase avec report", test4),
        ("Test 5 - Format abrégé", test5),
        ("Test 6 - Phrase complexe avec contexte", test6),
        ("Test 7 - Format français", test7),
        ("Test 8 - Phrase très informelle", test8)
    ]
    
    print("🧪 TESTS DE L'IA AMÉLIORÉE")
    print("=" * 60)
    print()
    
    for test_name, test_text in tests:
        print(f"📧 {test_name}")
        print("-" * 40)
        print(f"Texte : {test_text.strip()}")
        
        # Extraction de la date
        date_extracted = extract_delivery_date_intelligent(test_text)
        
        if date_extracted:
            print(f"✅ Date extraite : {date_extracted}")
        else:
            print("❌ Aucune date extraite")
        
        print()
    
    # Test de performance avec un email complexe
    print("🚀 TEST DE PERFORMANCE AVANCÉ")
    print("=" * 60)
    
    complex_email = """
    Bonjour,
    
    Suite à votre commande BSK2506CF0383, nous avons rencontré des difficultés.
    
    Initialement prévue pour le 10/10/2025, la livraison ne pourra pas être effectuée
    avant le 12/10/25 en raison d'un problème de stock.
    
    Nous nous excusons pour ce contretemps et faisons tout notre possible pour
    respecter cette nouvelle échéance du 12/10/2025.
    
    Cordialement,
    IMPRIMERIE AJDIR
    """
    
    print("📧 Email complexe avec plusieurs dates :")
    print(complex_email.strip())
    print()
    
    date_final = extract_delivery_date_intelligent(complex_email)
    print(f"🎯 Date finale extraite : {date_final}")
    
    # Vérification de la logique
    if date_final == "12/10/2025":
        print("✅ SUCCÈS : L'IA a correctement identifié la date la plus récente !")
    else:
        print("❌ ÉCHEC : L'IA n'a pas identifié la bonne date")

if __name__ == "__main__":
    test_extraction()
