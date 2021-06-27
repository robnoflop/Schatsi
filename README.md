# Schatsi
Dieses Projekt ist am Lehrstuhl Service Operation an der Universität Rostock angesiedelt.

# Release new SCHATSI version
1. Open "docker-compose.yml" and update image description. Naming convention = schiggy89/schatsi:<<YYMMDD>>.<<index>>.
2. Open cmd enter: docker build -t schiggy89/schatsi:<<YYMMDD>>.<<index>>
3. docker push schiggy89/schatsi:<<YYMMDD>>.<<index>>
