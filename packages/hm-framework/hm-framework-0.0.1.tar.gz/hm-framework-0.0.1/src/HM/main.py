from framework \
    import AutomationFramework


def main():
    automated = AutomationFramework()

    try:
        automated.setup()
        automated.execute()

    finally:
        automated.finish()


if __name__ == '__main__':
    main()
