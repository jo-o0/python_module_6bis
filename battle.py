from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    print("=== Testing Factory ===")
    creature = factory.create_base()
    print(f"{creature.describe()}")
    print(f"{creature.attack()}")
    print()
    evolved_creature = factory.create_evolved()
    print(f"{evolved_creature.describe()}")
    print(f"{evolved_creature.attack()}")


def battle(factory_a: CreatureFactory, factory_b: CreatureFactory) -> None:
    print("=== Testing Battle ===")
    creature_a = factory_a.create_base()
    creature_b = factory_b.create_base()

    print("=== FIGHT!!! ====")
    print(f"{creature_a.describe()} vs {creature_b.describe()}")
    print(f"{creature_a.attack()}")
    print(f"{creature_b.attack()}")


def battle_main() -> None:
    flame = FlameFactory()
    transform = TransformCreatureFactory()

    test_factory(flame)
    print()
    test_factory(transform)
    print()
    battle(flame, transform)
    print("\n=== End of program ===")


if __name__ == "__main__":
    battle_main()
