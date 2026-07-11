from log_parser import parse_log_file

def test_count():
    text = "2023-01-01 12:00:00 [INFO] 192.168.1.1 Message A\n2023-01-01 12:01:00 [WARN] 192.168.1.2 Message B\n2023-01-01 12:02:00 [ERROR] 192.168.1.3 Message C\n"
    stats = parse_log_file(text)
    assert stats["LINES"] == 3
    assert stats["INFO"] == 1
    assert stats["WARN"] == 1
    assert stats["ERROR"] == 1

def test_bug_confusion():
    # On crée un faux log "piège"
    # C'est un message [INFO], mais il contient le mot "ERROR" dedans.
    text = "2023-01-01 12:00:00 [INFO] 192.168.1.1 Ceci n'est pas une ERROR, juste une phrase.\n"
    
    stats = parse_log_file(text)

    # Vérifications :
    # Il doit y avoir 1 INFO (car c'est tagué [INFO])
    assert stats["INFO"] == 1
    # Il doit y avoir 0 ERROR (car le mot ERROR fait partie de la phrase)
    assert stats["ERROR"] == 0
